from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.notification.views import NotificationReadAPI, NotificationViewSet

router = DefaultRouter()
router.register("notifications", NotificationViewSet, basename='notifications')

read_view = NotificationReadAPI.as_view({"patch" : "partial_update"})

urlpatterns = [
    path("notifications/<int:pk>/read", read_view, name="notification-read")
]

urlpatterns += router.urls
