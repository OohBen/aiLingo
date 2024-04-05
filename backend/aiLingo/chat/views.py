from rest_framework import generics, status
from rest_framework.response import Response
from quizzes.models import Quiz
from quizzes.serializers import QuestionSerializer
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.conf import settings
import google.generativeai as genai
from rest_framework.permissions import IsAuthenticated

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    def parse_quiz_data(self, text: str):
        quiz_data = {}
        lines = text[text.find("___quiz!!!___"):].strip().split("\n")

        for line in lines:
            print(line)
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

        return quiz_data

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

        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

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
        prompt = f"""
                For newline characters inside table cells, use the special character sequence "\\n".
                You are a teacher and master in the {conversation.language.name} language. Use only markdown for outputting, including tables. For tables, use the following markdown rendering, :

                | Syntax      | Description |
                | ----------- | ----------- |
                | Header      | Title       |
                | Paragraph   | Text        |


                Your role is to teach and provide explanations without directing to outside sources. Provide your responses in markdown format.
                If the user asks for a quiz, FIRST add ___quiz!!!___ then generate a quiz with the following strict format:

                Quiz Title: <quiz_title>
                Duration: <duration_in_minutes>
                Passing Score: <passing_score_percentage>

                Then generate 5 multiple-choice questions for the quiz, each with the following strict format:

                q: <question_text>
                c1: <choice_1>
                e1: <explanation_for_choice_1_in_{home_language}>
                c2: <choice_2>
                e2: <explanation_for_choice_2_in_{home_language}>
                c3: <choice_3>
                e3: <explanation_for_choice_3_in_{home_language}>
                c4: <choice_4>
                e4: <explanation_for_choice_4_in_{home_language}>
                a: <correct_answer_choice_number>
                w: <worth_of_question_as_integer>

                Make sure to include all the required components for the quiz and each question. Provide the entire quiz in the specified strict format, with each question starting on a new line.

                Conversation history:
                {conversation_history}

                User: {user_message}
                AI Teacher:
                """

        response = model.generate_content(prompt)
        bot_response = response.text.replace("\n", "\\n")

        if "___quiz!!!___" in response.text:
            quiz_data = self.parse_quiz_data(response.text)
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
                
                bot_response += f"\n\nQuiz created successfully! You can access the quiz at: /quizzes/{quiz.id}"

        
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


