from django.db import models


class ChatQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def with_participant(self, user):
        return self.filter(participants=user)

    def created_by_user(self, user):
        return self.filter(created_by=user)

    def recent(self):
        return self.order_by("-updated_at")

    def with_title(self, title):
        return self.filter(title__icontains=title)


class ChatManager(models.Manager):
    def get_queryset(self):
        return ChatQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def with_participant(self, user):
        return self.get_queryset().with_participant(user)

    def created_by_user(self, user):
        return self.get_queryset().created_by_user(user)

    def recent(self):
        return self.get_queryset().recent()

    def with_title(self, title):
        return self.get_queryset().with_title(title)
