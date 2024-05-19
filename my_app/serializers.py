from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'name', 'profile_picture']
        read_only_fields = ['id', 'username']

class MessageSerializer(serializers.ModelSerializer):
    suggested_reply = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'text', 'media', 'created_at', 'replied_to', 'suggested_reply']

    def get_suggested_reply(self, obj):
        return obj.suggest_reply()

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'message_template']

class RecurringMessageSerializer(serializers.ModelSerializer):
    message = MessageSerializer()

    class Meta:
        model = RecurringMessage
        fields = ['id', 'message', 'recurrence_rule', 'next_send_time']