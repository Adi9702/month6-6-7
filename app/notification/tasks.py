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