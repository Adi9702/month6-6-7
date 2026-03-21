from django.db import transaction
from app.notification.models import Notification
from app.notification.tasks import deliver_notification

def publish_notification(
    *, user_id: int, 
    type: str, 
    title : str = "", 
    message : str
    ) -> Notification:
    with transaction.atomic():
        notif = Notification.objects.create(
            user_id=user_id,
            type = type,
            title=title,
            message=message
        )
        transaction.on_commit(lambda : deliver_notification.delay((notif.id)))

    return notif
