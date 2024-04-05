from django.urls import path
from .views import (
    LanguageCreateView,
    LanguageListView,
    LanguageRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", LanguageListView.as_view(), name="language-list"),
    path("create/", LanguageCreateView.as_view(), name="language-create"),
    path(
        "<int:pk>/",
        LanguageRetrieveUpdateDestroyView.as_view(),
        name="language-retrieve-update-destroy",
    ),
]
