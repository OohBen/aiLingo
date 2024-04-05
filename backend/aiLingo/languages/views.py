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
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superusers can create languages."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)
