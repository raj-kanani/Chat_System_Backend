from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'recurring-messages', RecurringMessageViewSet)
router.register(r'user-settings', UserSettingsViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/me/', UserRetrieveUpdateView.as_view(), name='user-detail'),
]