from django.db import models
from app.users.models import User

class NotificationType(models.TextChoices):
    ORDER_STATUS_CHANGED = "order_status_changed", "order status changed" 
    PRODUCT_STATUS_CHANGED = "product_status+_changed" , "products status changed"

class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="notifications" 
    )
    type = models.CharField(
        max_length=70,
        choices=NotificationType.choices
    )
    title = models.CharField(
        max_length=255
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)
    ctreated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.type    