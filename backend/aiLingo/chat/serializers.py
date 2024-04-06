from rest_framework import serializers

from languages.models import Language
from .models import Conversation, Message
from languages.serializers import LanguageSerializer


class ConversationSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "language", "title", "created_at"]

    def create(self, validated_data):
        language_id = validated_data.pop("language_id")
        language = Language.objects.get(id=language_id)
        title = validated_data.pop("title")
        conversation = Conversation.objects.create(language=language, title=title, **validated_data)
        return conversation
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "content", "timestamp"]
