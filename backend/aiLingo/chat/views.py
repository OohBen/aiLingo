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
        language_id = self.request.data.get('language')
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
            elif line.startswith("c:"):
                question_data["choices"].append(line.split(":")[1].strip())
            elif line.startswith("e:"):
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
            "When the user submits a request, analyze the text to identify if it is asking for a quiz by detecting keywords such as \"quiz\", \"test\", \"questionnaire\",  \"exam\", or any other phrases or words that would make you think the user is asking for a quiz.\n\nIf quiz-related keywords are detected:\n- Append the tag ___QUIZ___ at the top of the response to indicate a quiz-based response.\n- Format the quiz response to include exactly five questions, and ensure each quiz contains the following elements:\n  - Quiz Title\n  - Duration: Time allocated for completing the quiz (in minutes).\n  - Passing Score: Minimum score required to pass (as an integer).\n  - Questions (q:) in the user's home language, each followed by:\n    - Choices (c:): 4 multiple-choice options for the answer in the target language.\n    - Correct Answer (a:): The index of the correct choice (0-based index), varying the position of the correct answer.\n    - Explanations (e:): Explanation for why the correct answer is right, in the user's home language.\n    - Worth (w:): Points awarded for each correct answer.\n\nIf no quiz-related keywords are detected or if you can not make a quiz from the requested text then you are to :\n- Respond to the user's request as a regular chat interaction, providing relevant information, answers, or engaging in conversation based on the user's input.\n\nWhen making a quiz, make sure to follow the exact format of the examples and use a variety of correct answer positions, not just the first choice.",
            "input: Quiz on Basic Vocabulary (User's Home Language: French, Learning: Italian)",
            "output: ___QUIZ___\nQuiz Title: Test de vocabulaire italien de base\nDuration: 15\nPassing Score: 80\nq: Comment dit-on \"livre\" en italien ?\nc: libro\nc: penna\nc: quaderno\nc: tavolo\ne: 'Libro' est le mot italien pour 'livre'.\na: 0\nw: 10\nq: Quel est le mot italien pour \"eau\" ?\nc: latte\nc: succo\nc: acqua\nc: vino\ne: 'Acqua' est la traduction correcte de 'eau' en italien.\na: 2\nw: 10\nq: Traduisez \"maison\" en italien.\nc: macchina\nc: casa\nc: cane\nc: finestra\ne: 'Casa' signifie 'maison' en italien.\na: 1\nw: 10\nq: Comment dit-on \"pomme\" en italien ?\nc: banana\nc: arancia\nc: mela\nc: fragola\ne: 'Mela' est le mot italien pour 'pomme'.\na: 2\nw: 10\nq: Quel est le mot italien pour \"chien\" ?\nc: gatto\nc: cavallo\nc: uccello\nc: cane\ne: 'Cane' est le mot italien pour 'chien'.\na: 3\nw: 10",
            "input: What is the weather like today? (User's Home Language: English, Learning: Spanish)",
            "output: The weather today is sunny and warm, with clear skies and a gentle breeze. It's a perfect day to spend some time outdoors and enjoy the nice weather. Remember to stay hydrated and protect your skin from the sun if you plan to be outside for an extended period. You can say \"Hace sol y calor\" to describe sunny and hot weather in Spanish.",
            "conversation_history " + conversation_history,
            f"input: {user_message} (User's Home Language: {home_language}, Learning: {learning_language})",
            "output: ",
        ]

        prompt = "\n".join(prompt_parts)

        response = model.generate_content(prompt)

        if "___QUIZ___" in response.text:
            quiz_data = self.parse_generated_questions(response.text[response.text.find("___QUIZ___") + 11:])
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

            quiz_url = f"/quizzes/{quiz.id}/"
            bot_response = f"Quiz created successfully! You can take the quiz by clicking on this link: [Take the Quiz]({quiz_url})"
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
