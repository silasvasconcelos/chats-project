from rest_framework import serializers
from ..models import Message
from .user_serializer import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    chat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "chat_id",
            "content",
            "sender",
            "context_index",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
