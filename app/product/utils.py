from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app.product.models import Product

@receiver([post_save, post_delete], sender=Product)
def clear_product(sender, **kwatgs):
    cache.delete("product_list")