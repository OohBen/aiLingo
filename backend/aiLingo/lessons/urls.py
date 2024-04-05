from django.urls import path
from .views import (
    # LessonListCreateView,
    # LessonRetrieveUpdateDestroyView,
    UserLessonListCreateView,
    UserLessonRetrieveUpdateDestroyView,
)

urlpatterns = [
    # path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    # path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-retrieve-update-destroy'),
    path("", UserLessonListCreateView.as_view(), name="user-lesson-list-create"),
    path(
        "<int:pk>/",
        UserLessonRetrieveUpdateDestroyView.as_view(),
        name="user-lesson-retrieve-update-destroy",
    ),
]
