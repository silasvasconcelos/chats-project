from django.db import models


class MessageQuerySet(models.QuerySet):
    def for_chat(self, chat):
        return self.filter(chat=chat)

    def from_user(self, user):
        return self.filter(sender=user)

    def with_context(self):
        return self.exclude(context_index__isnull=True)

    def without_context(self):
        return self.filter(context_index__isnull=True)

    def recent(self):
        return self.order_by("-created_at")

    def oldest(self):
        return self.order_by("created_at")

    def between_dates(self, start_date, end_date):
        return self.filter(created_at__range=(start_date, end_date))


class MessageManager(models.Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def for_chat(self, chat):
        return self.get_queryset().for_chat(chat)

    def from_user(self, user):
        return self.get_queryset().from_user(user)

    def with_context(self):
        return self.get_queryset().with_context()

    def without_context(self):
        return self.get_queryset().without_context()

    def recent(self):
        return self.get_queryset().recent()

    def oldest(self):
        return self.get_queryset().oldest()

    def between_dates(self, start_date, end_date):
        return self.get_queryset().between_dates(start_date, end_date)
