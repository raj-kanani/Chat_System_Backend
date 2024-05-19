from .utils import send_otp
import datetime,random
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status,generics, permissions
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import *
from django.http import JsonResponse
from .serializers import *


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        print(phone)
        try:
            user = User.objects.get(phone=phone)
            # Generate OTP and update user record
            otp = random.randint(1000, 9999)

            user.otp = otp
            user.save()
            print(user.otp, 'OTP')
            send_otp(user.phone, otp)
            return Response("Successfully generated OTP", status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            user_ = User.objects.create(phone=phone)
            print(user_)

            otp = random.randint(1000, 9999)
            user_.otp = otp
            user_.is_passenger = True
            user_.save()
            send_otp(user_.phone, otp)
            return Response("Successfully generated OTP", status=status.HTTP_200_OK)
        else:
            return Response("Phone number is incorrect", status=status.HTTP_401_UNAUTHORIZED)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        otp = request.data['otp']
        print(otp)
        user = User.objects.get(otp=otp)

        if user:
            login(request, user)
            user.otp = None
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response("Please enter the correct OTP", status=status.HTTP_400_BAD_REQUEST)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

# chat functionality
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.save()
        chat.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    #  To running schedule message using cron :
    '''
        * * * * * /path/to/your/virtualenv/bin/python /path/to/your/project/manage.py send_scheduled_messages
    '''

    def perform_create(self, serializer):
        scheduled_at = serializer.validated_data.get('scheduled_at')
        if scheduled_at and scheduled_at > timezone.now():
            serializer.save(sender=self.request.user, sent=False)
        else:
            serializer.save(sender=self.request.user, sent=True)

    # message scheduling
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        scheduled_at = request.data.get('scheduled_at')
        if scheduled_at:
            return Response({'message': 'Message scheduled successfully'}, status=status.HTTP_201_CREATED)
        return response

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecurringMessageViewSet(viewsets.ModelViewSet):
    queryset = RecurringMessage.objects.all()
    serializer_class = RecurringMessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        message_data = data.pop('message')
        message_serializer = MessageSerializer(data=message_data)
        message_serializer.is_valid(raise_exception=True)
        message = message_serializer.save(sender=self.request.user)

        recurring_message = RecurringMessage.objects.create(
            message=message,
            recurrence_rule=data['recurrence_rule'],
            next_send_time=data['next_send_time']
        )
        serializer = self.get_serializer(recurring_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Enable sending messages to selected users.
class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)