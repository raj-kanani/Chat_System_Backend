from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import *


class Command(BaseCommand):
    help = 'Send scheduled messages and event-based messages'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Send scheduled messages
        scheduled_messages = Message.objects.filter(scheduled_at__lte=now, sent=False)
        for message in scheduled_messages:
            message.sent = True
            message.save()
            # Logic to send the message (e.g., notify the recipient)
            self.stdout.write(self.style.SUCCESS(f'Scheduled Message {message.id} sent'))

        # Send event-based messages
        today = now.date()
        events = Event.objects.filter(date=today)
        for event in events:
            chats = Chat.objects.all()  # Adjust this to select relevant chats if needed
            for chat in chats:
                for participant in chat.participants.all():
                    message = Message(
                        chat=chat,
                        sender=participant,  # Assuming the sender is a participant; adjust as needed
                        text=event.message_template,
                        created_at=now,
                        sent=True
                    )
                    message.save()
                    self.stdout.write(self.style.SUCCESS(f'Event Message {message.id} sent for event {event.name}'))
