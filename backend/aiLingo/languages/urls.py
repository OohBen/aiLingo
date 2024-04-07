from django.urls import path
from .views import (
    LanguageListCreateView,
    LanguageRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", LanguageListCreateView.as_view(), name="language-list"),
    path(
        "<int:pk>/",
        LanguageRetrieveUpdateDestroyView.as_view(),
        name="language-retrieve-update-destroy",
    ),
]
