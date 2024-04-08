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

    def parse_quiz_data(self, text: str):
        quiz_data = {}
        lines = text[text.find("___quiz!!!___"):].strip().split("\n")

        for line in lines:
            if line.startswith("Quiz Title:"):
                quiz_data["title"] = line.split("Quiz Title:")[1].strip()
            elif line.startswith("Duration:"):
                quiz_data["duration"] = int(line.split("Duration:")[1].strip())
            elif line.startswith("Passing Score:"):
                quiz_data["passing_score"] = int(line.split("Passing Score:")[1].strip())
            elif line.startswith("q:"):
                if "questions" not in quiz_data:
                    quiz_data["questions"] = []
                question_data = {}
                question_data["text"] = line.split("q:")[1].strip()
            elif line.startswith("c"):
                if "choices" not in question_data:
                    question_data["choices"] = []
                question_data["choices"].append(line.split("c")[1].strip())
            elif line.startswith("e"):
                if "explanations" not in question_data:
                    question_data["explanations"] = []
                question_data["explanations"].append(line.split("e")[1].strip())
            elif line.startswith("a:"):
                question_data["answer"] = int(line.split("a:")[1].strip())
            elif line.startswith("w:"):
                question_data["worth"] = int(line.split("w:")[1].strip())
                quiz_data["questions"].append(question_data)

        return quiz_data if "title" in quiz_data and "duration" in quiz_data and "passing_score" in quiz_data and "questions" in quiz_data else None
    
    def extract_topic_scores(self, text):
        print(text)
        topic_scores = json.loads(text.strip().replace("'", "\""))
        print(topic_scores)
        return topic_scores

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

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

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
            f"You are a teacher of the {learning_language} language. Reply in {home_language} and provide examples when teaching. Be supportive and helpful.",
            "Unless specified, generate 5 example questions.",
            "When giving the answer key to questions, ADD 888333 ANSWERKEY 888333, then on the next line, add the answers.",
            f"For newline characters inside table cells, use the special character sequence \"\\n\".",
            f"You are a teacher and master in the {learning_language} language. Use only markdown for outputting, including tables. For tables, use the following markdown rendering:",
            "\n| Syntax      | Description |\n| ----------- | ----------- |\n| Header      | Title       |\n| Paragraph   | Text        |",
            "Your role is to teach and provide explanations without directing to outside sources. Provide your responses in markdown format.",
            f"If the user asks for a quiz, FIRST add ___quiz!!!___ then generate a quiz with the following strict format:",
            "Quiz Title: <quiz_title>",
            "Duration: <duration_in_minutes>",
            "Passing Score: <passing_score_percentage>",
            "Then generate 5 multiple-choice questions for the quiz, each with the following strict format:",
            "q: <question_text>",
            "c1: <choice_1>",
            "e1: <explanation_for_choice_1_in_{home_language}>",
            "c2: <choice_2>",
            "e2: <explanation_for_choice_2_in_{home_language}>",
            "c3: <choice_3>",
            "e3: <explanation_for_choice_3_in_{home_language}>",
            "c4: <choice_4>",
            "e4: <explanation_for_choice_4_in_{home_language}>",
            "a: <correct_answer_choice_number>",
            "w: <worth_of_question_as_integer>",
            "Make sure to include all the required components for the quiz and each question. Provide the entire quiz in the specified strict format, with each question starting on a new line. If the user's message does not explicitly ask for a quiz, do not generate one.",
            "Here's an example of a generated quiz:",
            "___quiz!!!___",
            "Quiz Title: French Greetings",
            "Duration: 10",
            "Passing Score: 80",
            "q: How do you say \"Hello\" in French?",
            "c1: Bonjour",
            "e1: Correct! \"Bonjour\" means \"Hello\" in French.",
            "c2: Au revoir",
            "e2: \"Au revoir\" means \"Goodbye\" in French.",
            "c3: Merci",
            "e3: \"Merci\" means \"Thank you\" in French.",
            "c4: Bonsoir",
            "e4: \"Bonsoir\" means \"Good evening\" in French.",
            "a: 1",
            "w: 2",
            "q: How do you say \"Good morning\" in French?",
            "c1: Bonsoir",
            "e1: \"Bonsoir\" means \"Good evening\" in French.",
            "c2: Bonjour",
            "e2: \"Bonjour\" is a general greeting that can be used throughout the day.",
            "c3: Bon matin",
            "e3: Correct! \"Bon matin\" means \"Good morning\" in French.",
            "c4: Bonne nuit",
            "e4: \"Bonne nuit\" means \"Good night\" in French.",
            "a: 3",
            "w: 2",
            "q: What is the French word for \"please\"?",
            "c1: Merci",
            "e1: \"Merci\" means \"Thank you\" in French.",
            "c2: S'il vous plaît",
            "e2: Correct! \"S'il vous plaît\" means \"Please\" in French.",
            "c3: Oui",
            "e3: \"Oui\" means \"Yes\" in French.",
            "c4: Non",
            "e4: \"Non\" means \"No\" in French.",
            "a: 2",
            "w: 2",
            "q: How do you say \"My name is...\" in French?",
            "c1: Je m'appelle...",
            "e1: Correct! \"Je m'appelle...\" means \"My name is...\" in French.",
            "c2: Quel est votre nom?",
            "e2: \"Quel est votre nom?\" means \"What is your name?\" in French.",
            "c3: Comment allez-vous?",
            "e3: \"Comment allez-vous?\" means \"How are you?\" in French.",
            "c4: Merci",
            "e4: \"Merci\" means \"Thank you\" in French.",
            "a: 1",
            "w: 3",
            "q: What is the French phrase for \"Have a nice day\"?",
            "c1: Bonne journée",
            "e1: Correct! \"Bonne journée\" means \"Have a nice day\" in French.",
            "c2: Bon appétit",
            "e2: \"Bon appétit\" means \"Enjoy your meal\" in French.",
            "c3: Au revoir",
            "e3: \"Au revoir\" means \"Goodbye\" in French.",
            "c4: Bien sûr",
            "e4: \"Bien sûr\" means \"Of course\" in French.",
            "a: 1",
            "w: 3",
            "At the end of each message, add a dictionary with the topic scores for the message, explaining what subjects you taught during this interaction. For example:",
            "!!!TOPICS!!!: {'subjunctive': 0.1, 'travel vocab': 0.3, 'past perfect': 0.6}",
            "Make sure to include the entire dictionary with the topic scores at the end of each message, in the format of the example. It should be the last lines of the message. Begin the dictionary with !!!TOPICS!!!: and then the dictionary in the format shown.",
            f"Conversation history:\n{conversation_history}",
            f"User: {user_message}",
            "AI Teacher:",
        ]
        print(user_message)

        prompt = "\n".join(prompt_parts)

        response = model.generate_content(prompt)
        topics = response.text[response.text.find("!!!TOPICS!!!") + 13 :]
        response = response.text[: response.text.find("!!!TOPICS!!!")]
        bot_response = response.replace("\n", "\\n")

        if "___quiz!!!___" in response:
            quiz_data = self.parse_quiz_data(response)
            if quiz_data:
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
                
                # Reformat the quiz data for better user experience
                formatted_quiz_data = {
                    "id": quiz.id,
                    "title": quiz.title,
                    "duration": quiz.duration,
                    "passing_score": quiz.passing_score,
                    "questions": [],
                }
                for question in quiz.question_set.all():
                    formatted_question = {
                        "id": question.id,
                        "text": question.text,
                        "choices": question.choices,
                        "explanations": question.explanations,
                    }
                    formatted_quiz_data["questions"].append(formatted_question)

                bot_response += f"\n\nQuiz created successfully! You can access the quiz here: [Take Quiz](/quizzes/{quiz.id})"
                bot_response += f"\n\nQuiz Data:\n```json\n{json.dumps(formatted_quiz_data, indent=2)}\n```"
        
        bot_message_serializer = MessageSerializer(
            data={
                "conversation": conversation_id,
                "sender": "bot",
                "content": bot_response,
            }
        )
        bot_message_serializer.is_valid(raise_exception=True)
        bot_message_serializer.save()

        topic_scores = self.extract_topic_scores(topics)
        user_analytics, _ = UserAnalytics.objects.get_or_create(user=request.user)
        user_analytics.update_chat_analytics(conversation.language, len(user_message), topic_scores)

        return Response(bot_message_serializer.data, status=status.HTTP_201_CREATED)