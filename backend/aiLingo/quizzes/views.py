import re
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attempt, Question, Quiz
from .serializers import AttemptSerializer, QuestionSerializer, QuizSerializer
import google.generativeai as genai
from analytics.models import Analytics
from analytics.serializers import AnalyticsSerializer
from django.db.models import Avg

class CreateQuizView(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


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

        home_language = request.user.home_language.name if request.user.home_language else "English"
        prompt = f"Generate a quiz titled '{request.data['title']}' in the {request.data['language']} language with the following components:\n\n1. Duration in minutes (e.g., duration: 20)\n2. Passing score as a percentage (e.g., passing_score: 75)\n3. Five multiple-choice questions, each with the following strict format:\n\nq: <question_text>\nc1: <choice_1>\ne1: <explanation_for_choice_1_in_{home_language}>\nc2: <choice_2>\ne2: <explanation_for_choice_2_in_{home_language}>\nc3: <choice_3>\ne3: <explanation_for_choice_3_in_{home_language}>\nc4: <choice_4>\ne4: <explanation_for_choice_4_in_{home_language}>\na: <correct_answer_choice_number>\nw: <worth_of_question_as_integer>\n\nProvide the entire quiz in the specified strict format, with each question starting on a new line. The duration and passing score must be provided in the exact format specified above."

        response = model.generate_content(prompt)
        generated_text = response.text.strip()

        duration_match = re.search(r"duration:\s*(\d+)", generated_text)
        passing_score_match = re.search(r"passing_score:\s*(\d+)", generated_text)

        if duration_match:
            duration = int(duration_match.group(1))
        else:
            duration = 12  # Default duration if not provided by AI

        if passing_score_match:
            passing_score = int(passing_score_match.group(1))
        else:
            passing_score = 52  # Default passing score if not provided by AI

        quiz = serializer.save(user=self.request.user, duration=duration, passing_score=passing_score)

        generated_text = response.text.strip()

        duration_match = re.search(r"duration:\s*(\d+)", generated_text)
        passing_score_match = re.search(r"passing_score:\s*(\d+)", generated_text)

        if duration_match:
            quiz.duration = int(duration_match.group(1))
        if passing_score_match:
            quiz.passing_score = int(passing_score_match.group(1))
        quiz.save()

        questions_data = self.parse_generated_questions(generated_text)
        for question_data in questions_data:
            question_data["quiz"] = quiz.id
            serializer = QuestionSerializer(data=question_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)

    def parse_generated_questions(self, text):
        questions_data = []
        question_blocks = text.strip().split("\n\n")

        for block in question_blocks:
            question_data = {}
            lines = block.strip().split("\n")

            for line in lines:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    if key == "q":
                        question_data["text"] = value
                    elif key.startswith("c"):
                        if "choices" not in question_data:
                            question_data["choices"] = []
                        question_data["choices"].append(value)
                    elif key.startswith("e"):
                        if "explanations" not in question_data:
                            question_data["explanations"] = []
                        question_data["explanations"].append(value)
                    elif key == "a":
                        question_data["answer"] = int(value)
                    elif key == "w":
                        question_data["worth"] = int(value)

            if (
                "text" in question_data
                and "choices" in question_data
                and "answer" in question_data
                and "explanations" in question_data
                and "worth" in question_data
            ):
                questions_data.append(question_data)

        return questions_data

class QuizListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

class QuizQuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id = self.kwargs["quiz_id"]
        return Question.objects.filter(quiz_id=quiz_id)

class QuizAttemptView(generics.CreateAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        quiz_id = request.data.get("quiz")
        user_answers = request.data.get("user_answers")

        quiz = Quiz.objects.get(id=quiz_id)
        user = request.user

        total_score = 0
        max_score = 0

        for question_id, user_answer in user_answers.items():
            question = Question.objects.get(id=question_id)
            max_score += question.worth
            if question.answer == user_answer:
                total_score += question.worth

        score = (total_score / max_score) * 100 if max_score > 0 else 0
        attempt = Attempt.objects.create(user=user, quiz=quiz, score=score)
        serializer = self.get_serializer(attempt)

        quiz_count = Attempt.objects.filter(
            user=user, quiz__language=quiz.language
        ).count()
        average_score = (
            Attempt.objects.filter(user=user, quiz__language=quiz.language).aggregate(
                Avg("score")
            )["score__avg"]
            or 0
        )
        topic_preferences = {}

        for question in quiz.question_set.all():
            if question.answer == user_answers.get(str(question.id)):
                topic_preferences[question.text] = question.worth

        analytics_data = {
            "quiz_count": quiz_count,
            "average_score": average_score,
            "topic_preferences": topic_preferences,
        }

        if analytics_data is None:
            analytics_data = {}
        analytics_serializer = AnalyticsSerializer(
            data={"user": user.id, "data": analytics_data}
        )
        if analytics_serializer.is_valid(raise_exception=True):
            analytics_serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)