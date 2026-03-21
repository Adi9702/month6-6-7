from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.notification.models import Notification
from app.notification.serializers import NotificationSerializers

class NotificationViewSet(mixins.ListModelMixin,
                    GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializers

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-id")

class NotificationReadAPI(ViewSet):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, pk=None):
        notif = get_object_or_404(Notification, pk=pk, user=request.user)
        notif.is_read = True
        notif.save(update_fields=["is_read"])
        return Response({"ok": True}, status=status.HTTP_200_OK)