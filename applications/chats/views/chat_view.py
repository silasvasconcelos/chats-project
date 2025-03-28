from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Chat
from ..serializers import ChatSerializer
from django.db import models
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from ..repositories.chat_repository import ChatRepository


@extend_schema(
    tags=["Chats"],
    description="ViewSet for managing chat rooms and participants",
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Chat room ID",
        )
    ],
)
class ChatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing chat rooms and their participants.

    Provides CRUD operations for chat rooms and additional actions for managing participants.
    Users can only access chats they created or are participants in.
    """

    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    chat_repository = ChatRepository()

    def get_queryset(self):
        return Chat.objects.filter(
            models.Q(created_by=self.request.user)
            | models.Q(participants=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        description="Add a user as a participant to the chat room",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "ID of the user to add as participant",
                    }
                },
                "required": ["user_id"],
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "participant added"}
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "user_id is required"}
                },
            },
            404: {"description": "User not found"},
        },
    )
    @action(detail=True, methods=["post"])
    def add_participant(self, request, pk=None):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)

        user = get_object_or_404(User, id=user_id)
        chat = self.chat_repository.add_participant(pk, user)

        if not chat:
            return Response({"error": "Chat not found"}, status=404)

        return Response({"status": "participant added"})

    @extend_schema(
        description="Remove a user from the chat room participants",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "ID of the user to remove from participants",
                    }
                },
                "required": ["user_id"],
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "participant removed"}
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "user_id is required"}
                },
            },
            404: {"description": "User not found"},
        },
    )
    @action(detail=True, methods=["post"])
    def remove_participant(self, request, pk=None):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)

        user = get_object_or_404(User, id=user_id)
        chat = self.chat_repository.remove_participant(pk, user)

        if not chat:
            return Response({"error": "Chat not found"}, status=404)

        return Response({"status": "participant removed"})
