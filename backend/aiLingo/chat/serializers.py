from rest_framework import serializers

from languages.models import Language
from .models import Conversation, Message
from languages.serializers import LanguageSerializer


class ConversationSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = Conversation
        fields = ["id", "language", "created_at"]

    def create(self, validated_data):
        language = validated_data.pop("language")
        conversation = Conversation.objects.create(language=language, **validated_data)
        return conversation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "content", "timestamp"]
