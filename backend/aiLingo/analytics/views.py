from rest_framework import generics
from .models import Analytics
from .serializers import AnalyticsSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from rest_framework.response import Response

class AnalyticsView(generics.RetrieveUpdateAPIView):
    serializer_class = AnalyticsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj, _ = Analytics.objects.get_or_create(user=user)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        total_quizzes = request.user.quiz_set.count()
        average_score = request.user.attempt_set.aggregate(Avg('score'))['score__avg']

        data = serializer.data
        data['total_quizzes'] = total_quizzes
        data['average_score'] = average_score

        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)