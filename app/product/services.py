from django.db import transaction
from app.product.models import Order, OrderStatus
from app.notification.models import NotificationType
from app.notification.services import publish_notification

def set_order_status(*, order : Order, new_status : str, actor) -> Order:
    old_status = order.status

    if old_status == new_status:
        return order

    with transaction.atomic():
        order.status = new_status

        if getattr(actor, "is_manager", False):
            order.manager_by = actor

        order.save(update_fields=['status', "manager_by"])

        def _after_commit():
            publish_notification(
                user_id=order.user_id,
                type=NotificationType.ORDER_STATUS_CHANGED,
                title="Статус заказа изменен",
                message=f"Your order #{order.id}: {old_status} -> {new_status}"
            )

            if order.courier_id:
                publish_notification(
                    user_id=order.courier_id,
                    type=NotificationType.ORDER_STATUS_CHANGED,
                    title='Обноваление заказа',
                    message=f"Orders #{order.id} updated. New status: {new_status}"
                )
        
        transaction.on_commit(_after_commit)

    return order
