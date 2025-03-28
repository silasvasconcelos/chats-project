from rest_framework import serializers
from ..models import File
from .user_serializer import UserSerializer


class FileSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = File
        fields = [
            "id",
            "file",
            "file_name",
            "file_type",
            "file_size",
            "uploaded_by",
            "uploaded_at",
        ]
        read_only_fields = ["file_name", "file_type", "file_size", "uploaded_at"]
