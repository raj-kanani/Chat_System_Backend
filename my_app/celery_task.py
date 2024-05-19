from celery import shared_task
from django.utils import timezone
from .models import *
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_app.settings')

app = Celery('my_app')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@shared_task
def schedule_message(message_id, scheduled_time):
    message = Message.objects.get(id=message_id)
    if timezone.now() >= scheduled_time:
        message.sent = True
        message.save()
    else:
        schedule_message.apply_async((message_id, scheduled_time), eta=scheduled_time)
