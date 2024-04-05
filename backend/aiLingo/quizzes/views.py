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


class GenerateQuestionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def post(self, request, quiz_id):
        quiz_id = self.kwargs["quiz_id"]
        quiz = Quiz.objects.get(id=quiz_id)
        prompt = request.data["prompt"]
        language = quiz.language
        # Configure the Gemini AI API
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

        prompt_parts = [
            f"You are a teacher of the {language} language. Reply in {language} and make sure to provide examples of use cases when teaching. Be supportive and helpful. Unless specified, generate 5 example questions. When giving the answer key to questions, use the following format: 888333 ANSWERKEY 888333 followed by the answers on the next line.",
            f"input: {prompt}",
            "output: ",
        ]

        response = model.generate_content(prompt_parts)
        generated_text = response.text

        # Extract the generated question and answer key
        question_text = generated_text.split("888333 ANSWERKEY 888333")[0].strip()
        answer_key = generated_text.split("888333 ANSWERKEY 888333")[1].strip()

        question_data = {"quiz": quiz.id, "text": question_text, "answer": answer_key}

        if "choices" in generated_text:
            choices = generated_text.split("choices:")[1].strip().split("\n")
            question_data["choices"] = choices

        serializer = QuestionSerializer(data=question_data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save()

        return Response({"question": serializer.data}, status=status.HTTP_201_CREATED)


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


class GenerateQuestionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def post(self, request, quiz_id):
        quiz_id = self.kwargs["quiz_id"]
        quiz = Quiz.objects.get(id=quiz_id)
        prompt = request.data["prompt"]
        language = quiz.language
        # Configure the Gemini AI API
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

        prompt_parts = [
            f"You are a teacher of the {language} language. Reply in {language} and make sure to provide examples of use cases when teaching. Be supportive and helpful. Unless specified, generate 5 example questions. When giving the answer key to questions, use the following format: 888333 ANSWERKEY 888333 followed by the answers on the next line.",
            f"input: {prompt}",
            "output: ",
        ]

        response = model.generate_content(prompt_parts)
        generated_text = response.text

        # Extract the generated question and answer key
        question_text = generated_text.split("888333 ANSWERKEY 888333")[0].strip()
        answer_key = generated_text.split("888333 ANSWERKEY 888333")[1].strip()

        question_data = {"quiz": quiz.id, "text": question_text, "answer": answer_key}

        if "choices" in generated_text:
            choices = generated_text.split("choices:")[1].strip().split("\n")
            question_data["choices"] = choices

        serializer = QuestionSerializer(data=question_data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save()

        return Response({"question": serializer.data}, status=status.HTTP_201_CREATED)


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


class CreateQuizView(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        quiz = serializer.instance

        # Configure the Generative AI API
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

        home_language = (
            request.user.home_language.name if request.user.home_language else "English"
        )
        prompt = f"Generate 5 multiple-choice questions for a quiz titled '{quiz.title}' in the {quiz.language} language. Provide explanations for each answer choice in the user's home language: {home_language}. Also, include the worth of each question (an integer value) based on its difficulty and importance. Use the following strict format for each question:\n\nq: <question_text>\nc1: <choice_1>\ne1: <explanation_for_choice_1>\nc2: <choice_2>\ne2: <explanation_for_choice_2>\nc3: <choice_3>\ne3: <explanation_for_choice_3>\nc4: <choice_4>\ne4: <explanation_for_choice_4>\na: <correct_answer_choice_number>\nw: <worth_of_question>\n\nMake sure to include all the required components (q, c1, e1, c2, e2, c3, e3, c4, e4, a, w) for each question, and provide the correct answer as a choice number (1, 2, 3, or 4). Here's an example of the format for a single question:\n\nq: What is the capital of France?\nc1: London\ne1: London is the capital of the United Kingdom, not France.\nc2: Paris\ne2: Paris is the correct answer. It is the capital of France.\nc3: Berlin\ne3: Berlin is the capital of Germany, not France.\nc4: Madrid\ne4: Madrid is the capital of Spain, not France.\na: 2\nw: 5\n\nPlease generate the questions in this exact format, with each question on a new line."

        response = model.generate_content(prompt)

        generated_text = response.text.strip()

        # Extract the generated questions and answer choices
        questions_data = self.parse_generated_questions(generated_text)
        # Save the generated questions to the database
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

        # Update analytics based on question worth
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

        # Ensure analytics_data is not None
        if analytics_data is None:
            analytics_data = {}
        analytics_serializer = AnalyticsSerializer(
            data={"user": user.id, "data": analytics_data}
        )
        if analytics_serializer.is_valid(raise_exception=True):
            analytics_serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
