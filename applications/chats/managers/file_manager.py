from django.db import models


class FileQuerySet(models.QuerySet):
    def for_chat(self, chat):
        return self.filter(chat=chat)

    def uploaded_by_user(self, user):
        return self.filter(uploaded_by=user)

    def by_file_type(self, file_type):
        return self.filter(file_type=file_type)

    def recent(self):
        return self.order_by("-uploaded_at")

    def oldest(self):
        return self.order_by("uploaded_at")

    def with_name(self, name):
        return self.filter(file_name__icontains=name)

    def larger_than(self, size_bytes):
        return self.filter(file_size__gt=size_bytes)

    def smaller_than(self, size_bytes):
        return self.filter(file_size__lt=size_bytes)


class FileManager(models.Manager):
    def get_queryset(self):
        return FileQuerySet(self.model, using=self._db)

    def for_chat(self, chat):
        return self.get_queryset().for_chat(chat)

    def uploaded_by_user(self, user):
        return self.get_queryset().uploaded_by_user(user)

    def by_file_type(self, file_type):
        return self.get_queryset().by_file_type(file_type)

    def recent(self):
        return self.get_queryset().recent()

    def oldest(self):
        return self.get_queryset().oldest()

    def with_name(self, name):
        return self.get_queryset().with_name(name)

    def larger_than(self, size_bytes):
        return self.get_queryset().larger_than(size_bytes)

    def smaller_than(self, size_bytes):
        return self.get_queryset().smaller_than(size_bytes)
