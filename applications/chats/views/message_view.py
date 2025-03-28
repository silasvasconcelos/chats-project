from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Message, Chat
from ..serializers import MessageSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    tags=["Messages"],
    description="ViewSet for managing messages within chat rooms",
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
            description="Message ID",
        ),
    ],
)
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages within chat rooms.

    Provides CRUD operations for messages and a context action to retrieve messages
    by their context index. Users can only access messages from chats they are participants in.
    """

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_pk")
        return Message.objects.filter(
            chat_id=chat_id, chat__participants=self.request.user
        )

    def perform_create(self, serializer):
        chat_id = self.kwargs.get("chat_pk")
        chat = get_object_or_404(Chat, id=chat_id, participants=self.request.user)
        serializer.save(chat=chat, sender=self.request.user)

    @extend_schema(
        description="Retrieve messages by their context index",
        parameters=[
            OpenApiParameter(
                name="context_index",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Index to filter messages by context",
                required=True,
            )
        ],
        responses={
            200: {
                "type": "array",
                "items": {"$ref": "#/components/schemas/MessageSerializer"},
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "context_index is required"}
                },
            },
        },
    )
    @action(detail=False, methods=["get"])
    def context(self, request, chat_pk=None):
        context_index = request.query_params.get("context_index")
        if not context_index:
            return Response({"error": "context_index is required"}, status=400)

        messages = self.get_queryset().filter(context_index=context_index)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
