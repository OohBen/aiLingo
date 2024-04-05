from django.urls import path
from .views import (
    QuizAttemptView,
    QuizListCreateView,
    QuizRetrieveUpdateDestroyView,
    CreateQuizView,
    QuizQuestionsView,
)

urlpatterns = [
    path("", QuizListCreateView.as_view(), name="quiz-list-create"),
    path(
        "<int:pk>/",
        QuizRetrieveUpdateDestroyView.as_view(),
        name="quiz-retrieve-update-destroy",
    ),

    path("create/", CreateQuizView.as_view(), name="create-quiz"),
    path(
        "<int:quiz_id>/questions/", QuizQuestionsView.as_view(), name="quiz-questions"
    ),
    path("attempt/", QuizAttemptView.as_view(), name="quiz-attempt"),
]
