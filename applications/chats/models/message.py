from django.db import models
from django.contrib.auth import get_user_model
from ..managers import MessageManager

User = get_user_model()


class Message(models.Model):
    chat = models.ForeignKey(
        "chats.Chat", on_delete=models.CASCADE, related_name="messages"
    )
    content = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    context_index = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}"
