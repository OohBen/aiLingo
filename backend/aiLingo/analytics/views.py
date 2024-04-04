from rest_framework import generics
from .models import Analytics
from .serializers import AnalyticsSerializer

class AnalyticsView(generics.RetrieveUpdateAPIView):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer

    def get_object(self):
        user = self.request.user
        obj, _ = Analytics.objects.get_or_create(user=user)
        return obj