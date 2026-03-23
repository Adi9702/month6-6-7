from django.urls import path

from app.notification.consumer import NotificationConsumer

websocket_urlpatterns = [
    path("ws/notification/", NotificationConsumer.as_asgi()),
]