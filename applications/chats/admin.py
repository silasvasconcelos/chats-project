# Register your models here.

from django.contrib import admin
from .models import Chat, Message, File


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("title", "prompt", "created_by__username")
    filter_horizontal = ("participants",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "sender", "context_index", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "context_index")
    search_fields = ("content", "sender__username", "chat__title")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "chat",
        "file_type",
        "file_size",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = ("file_type", "uploaded_at")
    search_fields = ("file_name", "chat__title", "uploaded_by__username")
    readonly_fields = ("file_name", "file_type", "file_size", "uploaded_at")
    ordering = ("-uploaded_at",)
