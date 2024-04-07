from rest_framework import generics
from .models import Language
from .serializers import LanguageSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class LanguageListCreateView(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer



    


