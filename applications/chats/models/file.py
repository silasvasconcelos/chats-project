from django.db import models
from django.contrib.auth import get_user_model
from ..managers import FileManager
import os

User = get_user_model()


def get_file_path(instance, filename):
    return f"chat_files/{instance.chat_id}/{filename}"


class File(models.Model):
    chat = models.ForeignKey(
        "chats.Chat", on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to=get_file_path)
    file_name = models.CharField(max_length=500)
    file_type = models.CharField(max_length=100)
    file_size = models.IntegerField()  # Size in bytes
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_files"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = FileManager()

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.file_name or f"File {self.id}"

    def save(self, *args, **kwargs):
        self.file_name = os.path.basename(self.file.name)
        self.file_type = self.file.content_type
        self.file_size = self.file.size
        super().save(*args, **kwargs)
