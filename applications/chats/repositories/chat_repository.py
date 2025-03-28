from typing import List, Optional
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from ..models.chat import Chat

User = get_user_model()


class ChatRepository:
    def __init__(self):
        self.model = Chat

    def create(
        self,
        title: str,
        created_by: User,
        prompt: str = "",
        is_active: bool = True,
        participants: Optional[List[User]] = None,
    ) -> Chat:
        """
        Create a new chat instance.

        Args:
            title: Chat title
            created_by: User who created the chat
            prompt: Initial prompt (optional)
            is_active: Whether the chat is active
            participants: List of participants (optional)

        Returns:
            Created Chat instance
        """
        chat = self.model.objects.create(
            title=title,
            prompt=prompt,
            is_active=is_active,
            created_by=created_by,
        )

        if participants:
            chat.participants.set(participants)

        return chat

    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        """
        Retrieve a chat by its ID.

        Args:
            chat_id: ID of the chat to retrieve

        Returns:
            Chat instance or None if not found
        """
        return self.model.objects.filter(id=chat_id).first()

    def get_active_chats(self) -> QuerySet[Chat]:
        """
        Get all active chats.

        Returns:
            QuerySet of active chats
        """
        return self.model.objects.active()

    def get_user_chats(self, user: User) -> QuerySet[Chat]:
        """
        Get all chats where the user is either creator or participant.

        Args:
            user: User to get chats for

        Returns:
            QuerySet of user's chats
        """
        return self.model.objects.filter(
            models.Q(created_by=user) | models.Q(participants=user)
        ).distinct()

    def get_recent_chats(self, limit: int = 10) -> QuerySet[Chat]:
        """
        Get most recently updated chats.

        Args:
            limit: Maximum number of chats to return

        Returns:
            QuerySet of recent chats
        """
        return self.model.objects.recent()[:limit]

    def update_chat(
        self,
        chat_id: int,
        title: Optional[str] = None,
        prompt: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[Chat]:
        """
        Update a chat's attributes.

        Args:
            chat_id: ID of the chat to update
            title: New title (optional)
            prompt: New prompt (optional)
            is_active: New active status (optional)

        Returns:
            Updated Chat instance or None if not found
        """
        chat = self.get_by_id(chat_id)
        if not chat:
            return None

        update_fields = []
        if title is not None:
            chat.title = title
            update_fields.append("title")
        if prompt is not None:
            chat.prompt = prompt
            update_fields.append("prompt")
        if is_active is not None:
            chat.is_active = is_active
            update_fields.append("is_active")

        if update_fields:
            chat.save(update_fields=update_fields)

        return chat

    def add_participant(self, chat_id: int, user: User) -> Optional[Chat]:
        """
        Add a participant to a chat.

        Args:
            chat_id: ID of the chat
            user: User to add as participant

        Returns:
            Updated Chat instance or None if not found
        """
        chat = self.get_by_id(chat_id)
        if not chat:
            return None

        chat.participants.add(user)
        return chat

    def remove_participant(self, chat_id: int, user: User) -> Optional[Chat]:
        """
        Remove a participant from a chat.

        Args:
            chat_id: ID of the chat
            user: User to remove from participants

        Returns:
            Updated Chat instance or None if not found
        """
        chat = self.get_by_id(chat_id)
        if not chat:
            return None

        chat.participants.remove(user)
        return chat

    def delete_chat(self, chat_id: int) -> bool:
        """
        Delete a chat.

        Args:
            chat_id: ID of the chat to delete

        Returns:
            True if deleted, False if not found
        """
        chat = self.get_by_id(chat_id)
        if not chat:
            return False

        chat.delete()
        return True

    def search_chats(self, query: str) -> QuerySet[Chat]:
        """
        Search chats by title.

        Args:
            query: Search query string

        Returns:
            QuerySet of matching chats
        """
        return self.model.objects.with_title(query)
