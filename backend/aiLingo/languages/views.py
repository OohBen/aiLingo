from rest_framework import generics
from .models import Language
from .serializers import LanguageSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class LanguageListView(generics.ListAPIView):
    permission_classes = []
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageCreateView(generics.CreateAPIView):
    serializer_class = LanguageSerializer
    permission_classes = []
    


