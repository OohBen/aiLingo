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

        home_language = (
            request.user.home_language.name if request.user.home_language else "English"
        )
        learning_language = conversation.language.name

        def generate_quiz(description):
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

            model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config, safety_settings=safety_settings)

            prompt = f"""
            Generate a quiz for {home_language} speakers learning {learning_language}.
            The quiz should be focused on {description}.
            The quiz should have 5 multiple-choice questions with 4 options each.
            Include the quiz title, duration in minutes, and passing score as an integer.
            The questions and explanations should be in the user's home language, and the answer choices should be in the target language.
            For each question, provide an explanation for the correct answer in the user's home language.
            Specify the point value of each question as an integer.
            Format the quiz as a JSON object with the following structure:
            {{
                "title": "Quiz Title",
                "duration": 10,
                "passing_score": 80,
                "questions": [
                    {{
                        "text": "Question 1 text",
                        "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
                        "answer": 0,
                        "explanation": "Explanation for correct answer",
                        "worth": 10
                    }},
                    ...
                ]
            }}
            """

            response = model.generate_content(prompt)
            return response.text

        tools = [
            {
                "function_declarations": [
                    {
                        "name": "generate_quiz",
                        "description": "Generates a quiz based on a given description.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "description": "A description of the topic or focus of the quiz."
                                }
                            },
                            "required": ["description"]
                        }
                    }
                ]
            }
        ]

        conversation_messages = Message.objects.filter(
            conversation=conversation
        ).order_by("timestamp")
        conversation_history = "\n".join(
            [
                f"{message.sender}: {message.content}"
                for message in conversation_messages
            ]
        )
        prompt_parts = [
            "You are a language learning assistant helping users learn a new language through conversation and quizzes.",
            f"The user's home language is {home_language}, and they are learning {learning_language}.",
            "If the user asks for a quiz or requests to test their knowledge, generate a quiz using the generate_quiz function.",
            "If the user's request is unclear or ambiguous, ask for clarification before generating a quiz.",
            "If the user's message does not appear to be requesting a quiz, provide a helpful response without generating a quiz.",
            "conversation_history:",
            conversation_history,
            f"user: {user_message}",
            "assistant:",
        ]

        prompt = "\n".join(prompt_parts)

        response = model.generate_content(prompt, tools=tools)

        if "function_call" in response.text:
            quiz_data = json.loads(generate_quiz(response.text["function_call"]["args"]["description"]))
            quiz = Quiz.objects.create(
                language=conversation.language,
                user=request.user,
                title=quiz_data["title"],
                duration=quiz_data["duration"],
                passing_score=quiz_data["passing_score"],
            )
            for question_data in quiz_data["questions"]:
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