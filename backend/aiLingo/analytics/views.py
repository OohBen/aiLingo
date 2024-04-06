from rest_framework import generics
from .models import UserAnalytics
from .serializers import UserAnalyticsSerializer
from rest_framework.permissions import IsAuthenticated

class UserAnalyticsView(generics.RetrieveAPIView):
    serializer_class = UserAnalyticsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj, _ = UserAnalytics.objects.get_or_create(user=user)
        return obj