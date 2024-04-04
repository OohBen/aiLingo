from rest_framework import serializers
from .models import Lesson, UserLesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'language', 'title', 'content']

class UserLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLesson
        fields = ['id', 'user', 'lesson', 'completed']