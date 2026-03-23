from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
from django.utils import timezone
from app.notification.models import Notification

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def deliver_notification(self, notification_id : int) -> None:
    notif = Notification.objects.filter(id=notification_id).first()

    if not notif:
        return

    if notif.delivered_at:
        return

    notif.delivered_at = timezone.now()
    notif.save(update_fields=["delivered_at"])

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{notif.user_id}",
        {
            "type": "send_notification",
            "data" : {
                "id": notif.id,
                "title": notif.title,
                "message": notif.message,
                "type": notif.type,
                "created_at": notif.created_at.isoformat(),
            }
        }
    )