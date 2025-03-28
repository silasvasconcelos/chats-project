from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from applications.chats.models import Chat, Message
from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generates sample chats with messages for testing purposes"

    def handle(self, *args, **options):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "test@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password("testpass123")
            user.save()
            self.stdout.write(self.style.SUCCESS("Created test user"))

        # Generate 5 chats
        for i in range(5):
            chat = Chat.objects.create(
                title=fake.sentence(),
                prompt=fake.paragraph(),
                created_by=user,
                is_active=True,
            )
            chat.participants.add(user)

            # Generate 30 messages for each chat
            for j in range(30):
                # Create messages with random timestamps within the last 7 days
                random_days = fake.random_int(min=0, max=7)
                random_hours = fake.random_int(min=0, max=24)
                random_minutes = fake.random_int(min=0, max=60)

                created_at = timezone.now() - timedelta(
                    days=random_days, hours=random_hours, minutes=random_minutes
                )

                Message.objects.create(
                    chat=chat,
                    content=fake.paragraph(),
                    sender=user,
                    context_index=j,
                    created_at=created_at,
                )

            self.stdout.write(
                self.style.SUCCESS(f'Created chat "{chat.title}" with 30 messages')
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully generated 5 chats with 30 messages each")
        )
