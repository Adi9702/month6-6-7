from django.db.models.signals import pre_save
from django.dispatch import receiver
from app.product.models import Product
from app.notification_ts import send_telegram_message

@receiver(pre_save, sender=Product)
def notify_product_activade(sender, instance : Product, **kwargs):
    if not instance.pk:
        return

    old = Product.objects.filter(pk=instance.pk).only("is_active").first()
    if not old:
        return

    if old.is_active is False and instance.is_active is True:
        chat_id = instance.user.telegram_chat_id
        if chat_id:
            send_telegram_message(
                chat_id,
                f"Ваш товар одобрен!\n{instance.title}"
            )