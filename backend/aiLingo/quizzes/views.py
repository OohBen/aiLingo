import re
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attempt, Question, Quiz
from .serializers import AttemptSerializer, QuestionSerializer, QuizSerializer
import google.generativeai as genai
from analytics.models import UserAnalytics

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
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

        prompt_parts = [
            "You are a teacher of the language mentioned in the prompt. Reply in the language of the prompt and make sure to have examples of use cases when teaching. Be supportive and helpful.",
            "Unless specified, generate 5 example questions.",
            "When giving the answer key to questions, ADD 888333 ANSWERKEY 888333, then on the next line, add the answers.",
            f"Create a quiz titled '{request.data['title']}' in the {request.data['language']} language.",
        ]

        prompt = "\n".join(prompt_parts)

        response = model.generate_content(prompt)
        generated_text = response.result.text.strip()

        quiz = serializer.save(user=self.request.user)

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
                    elif key == "a":
                        question_data["answer"] = int(value)

            if "text" in question_data and "choices" in question_data and "answer" in question_data:
                questions_data.append(question_data)

        return questions_data

class QuizListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

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

        score = (total_score / max_score) * 100
        attempt = Attempt.objects.create(user=user, quiz=quiz, score=score)
        serializer = self.get_serializer(attempt)

        topic_scores = {}
        for question in quiz.question_set.all():
            if question.answer == user_answers.get(str(question.id)):
                topic_scores[question.text] = question.worth

        user_analytics, _ = UserAnalytics.objects.get_or_create(user=user)
        user_analytics.update_quiz_analytics(quiz.language, score, topic_scores)

        return Response(serializer.data, status=status.HTTP_201_CREATED)