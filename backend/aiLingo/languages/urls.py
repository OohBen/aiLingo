from django.urls import path
from .views import (
    LanguageListCreateView,
    LanguageRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', LanguageListCreateView.as_view(), name='language-list-create'),
    path('<int:pk>/', LanguageRetrieveUpdateDestroyView.as_view(), name='language-retrieve-update-destroy'),
]