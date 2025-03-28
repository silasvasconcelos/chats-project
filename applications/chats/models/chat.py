from django.db import models
from django.contrib.auth import get_user_model
from ..managers import ChatManager

User = get_user_model()


class Chat(models.Model):
    title = models.CharField(max_length=255, blank=True)
    prompt = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    participants = models.ManyToManyField(User, related_name="participants_chats")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ChatManager()

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title or f"Chat {self.id}"
