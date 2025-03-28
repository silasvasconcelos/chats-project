from rest_framework import serializers
from ..models import Chat
from .user_serializer import UserSerializer
from .message_serializer import MessageSerializer
from .file_serializer import FileSerializer


class ChatSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Chat
        fields = [
            "id",
            "title",
            "prompt",
            "is_active",
            "created_by",
            "participants",
            "participant_ids",
            "messages",
            "files",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids", [])
        chat = Chat.objects.create(
            created_by=self.context["request"].user, **validated_data
        )
        if participant_ids:
            chat.participants.set(participant_ids)
        return chat

    def update(self, instance, validated_data):
        participant_ids = validated_data.pop("participant_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if participant_ids is not None:
            instance.participants.set(participant_ids)
        return instance
