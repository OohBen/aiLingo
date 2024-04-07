from rest_framework import serializers
from .models import Question, Quiz, Attempt


class QuestionSerializer(serializers.ModelSerializer):
    #how to make quiz add after the rest is but pass the is_valid() test
    
    class Meta:
        model = Question
        fields = ["id", "quiz", "text", "choices", "answer", "explanations", "worth"]
        extra_kwargs = {
            "quiz": {"required": False},
        }

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'language', 'title', 'duration', 'passing_score', 'questions']


class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ["id", "user", "quiz", "score", "date"]
