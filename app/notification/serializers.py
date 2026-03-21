from rest_framework import serializers 
from app.notification.models import Notification

class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'title',
            'message', "is_read", "delivered_at",
            'ctreated_at'
        ]