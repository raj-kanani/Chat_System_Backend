from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    phone = models.CharField(max_length=10, unique=True, blank=True, null=True, validators=[RegexValidator(
        regex=r"^\d{10}", message="Phone number must be 10 digits only.")])
    otp = models.CharField(max_length=6, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    auto_sending_enabled = models.BooleanField(default=True)
    recurring_messages_enabled = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['phone']

class Chat(models.Model):
    participants = models.ManyToManyField(User)

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    message_template = models.TextField()

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.SET_NULL)

    def suggest_reply(self):
        return "Thanks for your message!" if self.text else "Nice media!"


class RecurringMessage(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    recurrence_rule = models.CharField(max_length=255)  # e.g., 'daily', 'weekly', 'monthly'
    next_send_time = models.DateTimeField()