from rest_framework import serializers
from .models import UserAnalytics

class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalytics
        fields = ['user', 'language_progress', 'quiz_analytics', 'chat_analytics']