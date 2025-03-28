from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import File, Chat
from ..serializers import FileSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    tags=["Files"],
    description="ViewSet for managing files within chat rooms",
    parameters=[
        OpenApiParameter(
            name="chat_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="ID of the chat room",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="File ID",
        ),
    ],
)
class FileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing files within chat rooms.

    Provides CRUD operations for files and a download action.
    Users can only access files from chats they are participants in.
    """

    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_pk")
        return File.objects.filter(
            chat_id=chat_id, chat__participants=self.request.user
        )

    def perform_create(self, serializer):
        chat_id = self.kwargs.get("chat_pk")
        chat = get_object_or_404(Chat, id=chat_id, participants=self.request.user)
        serializer.save(chat=chat, uploaded_by=self.request.user)

    @extend_schema(
        description="Download a file from the chat room",
        responses={
            200: {
                "type": "string",
                "format": "binary",
                "description": "The file content with appropriate headers for download",
            },
            500: {
                "type": "object",
                "properties": {"error": {"type": "string", "example": "Error message"}},
            },
        },
    )
    @action(detail=True, methods=["get"])
    def download(self, request, chat_pk=None, pk=None):
        file_obj = self.get_object()
        try:
            response = Response()
            response["Content-Disposition"] = (
                f'attachment; filename="{file_obj.file_name}"'
            )
            response["Content-Type"] = file_obj.file_type
            response["X-Accel-Buffering"] = "no"
            return response
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
