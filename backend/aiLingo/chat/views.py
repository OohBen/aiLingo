import json
from rest_framework import generics, status
from rest_framework.response import Response
from languages.models import Language
from quizzes.models import Quiz
from quizzes.serializers import QuestionSerializer
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.conf import settings
import google.generativeai as genai
from rest_framework.permissions import IsAuthenticated
from analytics.models import UserAnalytics

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        language_id = self.request.data.get('language', {}).get('id')
        title = self.request.data.get('title')
        serializer.save(user=self.request.user, language_id=language_id, title=title)
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def parse_generated_questions(self, text):
        questions_data = []
        lines = text.split("\n")
        title = ""
        duration = 0
        passing_score = 0
        question_data = {}
        for line in lines:
            if line.startswith("Quiz Title:"):
                title = line.split(":")[1].strip()
            elif line.startswith("Duration:"):
                duration = int(line.split(":")[1].strip())
            elif line.startswith("Passing Score:"):
                passing_score_str = line.split(":")[1].strip()
                passing_score = int(passing_score_str)
            elif line.startswith("q:"):
                if question_data:
                    questions_data.append(question_data)
                    question_data = {}
                question_data["text"] = line.split(":")[1].strip()
                question_data["choices"] = []
                question_data["explanations"] = []
            elif line.startswith("c"):
                question_data["choices"].append(line.split(":")[1].strip())
            elif line.startswith("e"):
                question_data["explanations"].append(line.split(":")[1].strip())
            elif line.startswith("a:"):
                question_data["answer"] = int(line.split(":")[1].strip())
            elif line.startswith("w:"):
                question_data["worth"] = int(line.split(":")[1].strip())

        if question_data:
            questions_data.append(question_data)

        return {
            "title": title,
            "duration": duration,
            "passing_score": passing_score,
            "questions": questions_data,
        }

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]
        return Message.objects.filter(conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs["conversation_id"]
        conversation = Conversation.objects.get(id=conversation_id)
        user_message = request.data["content"]

        user_message_serializer = MessageSerializer(
            data={
                "conversation": conversation_id,
                "sender": "user",
                "content": user_message,
            }
        )
        user_message_serializer.is_valid(raise_exception=True)
        user_message_serializer.save()

        genai.configure(api_key=settings.GOOGLE_GENERATIVE_AI_API_KEY)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config,  safety_settings=safety_settings)

        conversation_messages = Message.objects.filter(
            conversation=conversation
        ).order_by("timestamp")
        conversation_history = "\n".join(
            [
                f"{message.sender}: {message.content}"
                for message in conversation_messages
            ]
        )
        home_language = (
            request.user.home_language.name if request.user.home_language else "English"
        )
        learning_language = conversation.language.name
        prompt_parts = [
        "When the user submits a request:The AI should analyze the text to identify if the request is asking for a quiz, by detecting keywords such as \"quiz\", \"test\", \"questionnaire\", or \"exam\" ora.If quiz-related keywords are detected:Append the tag ___QUIZ___ at the top of the response to indicate a quiz-based response.Format the quiz response to include exactly five questions, and ensure each quiz contains the following elements:Quiz TitleDuration: Time allocated for completing the quiz (in minutes).Passing Score: Minimum score required to pass (in percentage).Questions (q:): Each followed by:Choices (c:): Multiple-choice options for the answer.Correct Answer (a:): The index of the correct choice.Explanations (e:): Explanation for why the correct answer is right.Worth (w:): Points awarded for each correct answer.If no quiz-related keywords are detected:Directly respond to the user’s query with information or answers relevant to the request without any quiz formatting. When making a quiz make sure to follow the exact format of the examples",
        "input: Quiz on Basic  Vocabulary (User's Home Language: English, Learning: French)",
        "output: ___QUIZ___\nQuiz Title: Basic French Vocabulary Test\nDuration: 15 minutes\nPassing Score: 80\n\nq: In English , \"apple\" translates to what in French?\nc: Pomme\nc: Poire\nc: Pêche\ne: 'Pomme' is the French word for 'apple.'\na: 1\nw: 10\n\nq: What is the French term for \"book\", if your home language is English?\nc: Livre\nc: Écriture\nc: Page\ne: 'Livre' is the correct translation for 'book' in French.\na: 1\nw: 10\n\nq: If \"cat\" is in English, what is the equivalent in French?\nc: Chat\nc: Chien\nc: Cheval\ne: 'Chat' means 'cat' in French.\na: 1\nw: 10\n\nq: Translate \"sun\" from English to French.\nc: Soleil\nc: Lune\nc: Étoile\ne: 'Soleil' is the word for 'sun' in French.\na: 1\nw: 10\n\nq: How do you say \"water\" in French, considering you speak English?\nc: Eau\nc: Vin\nc: Bière\ne: 'Eau' is the French word for 'water.'\na: 1\nw: 10",
        "input: What's the word for 'book'? (User's Home Language: English, Learning: German)",
        "output: The German word for 'book' is 'Buch",
        "input: \"Could you create a quiz about basic phrases for me?\" (User's Home Language: English, Learning: Italian)",
        "output: ___QUIZ___\nQuiz Title: Basic Italian Phrases Quiz\nDuration: 15 minutes\nPassing Score: 80\n\nq: How do you say \"Good morning\" in Italian, starting from English?\nc: Buon giorno\nc: Buona sera\nc: Buona notte\ne: 'Buon giorno' translates as 'Good morning' in Italian.\na: 1\nw: 10\n\nq: Translate \"Thank you\" from English to Italian.\nc: Grazie\nc: Prego\nc: Scusa\ne: 'Grazie' means 'Thank you' in Italian.\na: 1\nw: 10\n\nq: What is \"I love you\" in Italian, if you're an English speaker?\nc: Ti amo\nc: Ti odio\nc: Ti aspetto\ne: 'Ti amo' is Italian for 'I love you.'\na: 1\nw: 10\n\nq: How to express \"Please\" in Italian when speaking English?\nc: Per favore\nc: Per piacere\nc: Per nulla\ne: Both 'Per favore' and 'Per piacere' can be used to say 'Please' in Italian, but 'Per favore' is more common.\na: 1\nw: 10\n\nq: What is the Italian word for \"yes\", knowing English?\nc: Sì\nc: No\nc: Forse\ne: 'Sì' is the Italian word for 'yes.'\na: 1\nw: 10",
        "conversation_history " + conversation_history,
        f"input: {user_message} (User's Home Language: {home_language}, Learning: {learning_language})",
        "output: ",
        ]
        pr
        prompt = "\n".join(prompt_parts)

        response = model.generate_content(prompt)
        
        if "___quiz!!!___" in response.text:
            quiz_data = self.parse_generated_questions(response.text[response.text.find("___quiz!!!___") + 13 :])
            quiz = Quiz.objects.create(
                language=conversation.language,
                user=request.user,
                title=quiz_data["title"],
                duration=quiz_data["duration"],
                passing_score=quiz_data["passing_score"],
            )
            questions_data = quiz_data["questions"]
            for question_data in questions_data:
                question_data["quiz"] = quiz.id
                serializer = QuestionSerializer(data=question_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            bot_response = f"Quiz created successfully! You can start the quiz at [/quizzes/{quiz.id}/](/quizzes/{quiz.id}/)"
        else:
            bot_response = response.text.replace("\n", "\\n")

        bot_message_serializer = MessageSerializer(
            data={
                "conversation": conversation_id,
                "sender": "bot",
                "content": bot_response,
            }
        )
        bot_message_serializer.is_valid(raise_exception=True)
        bot_message_serializer.save()

        return Response(bot_message_serializer.data, status=status.HTTP_201_CREATED)