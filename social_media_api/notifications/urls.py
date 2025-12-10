# notifications/urls.py
from django.urls import path
from .views import NotificationListAPIView, mark_notification_read

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notifications-list'),
    path('<int:pk>/read/', mark_notification_read, name='notification-mark-read'),
]
