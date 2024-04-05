from django.urls import path
from .views import (
    CreateQuizView,
    GenerateQuestionView,
    QuizAttemptView,
    QuizListCreateView,
    QuizQuestionsView,
    QuizRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", QuizListCreateView.as_view(), name="quiz-list-create"),
    path(
        "<int:pk>/",
        QuizRetrieveUpdateDestroyView.as_view(),
        name="quiz-retrieve-update-destroy",
    ),
    path(
        "<int:quiz_id>/generate-question/",
        GenerateQuestionView.as_view(),
        name="generate-question",
    ),
    path("create/", CreateQuizView.as_view(), name="create-quiz"),
    path(
        "<int:quiz_id>/questions/", QuizQuestionsView.as_view(), name="quiz-questions"
    ),
    path("attempt/", QuizAttemptView.as_view(), name="quiz-attempt"),
]
