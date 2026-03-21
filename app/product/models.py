from django.db import models
import uuid
from app.users.models import User

class Category(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Название'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорий'

class Models(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Название'
    )
    category = models.ForeignKey(
        Category, verbose_name='Category',
        on_delete=models.CASCADE,
        related_name='category', 
        blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модел'
        verbose_name_plural = 'Модели'

class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_porduct'
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='UUID'
    )
    category = models.ForeignKey(
        Category, verbose_name='Category',
        on_delete=models.CASCADE,
        related_name='category_product', 
        blank=True, null=True
    )
    model = models.ForeignKey(
        Models, verbose_name='models',
        on_delete=models.CASCADE,
        related_name='models_product', 
        blank=True, null=True
    )
    title = models.CharField(
        max_length=155,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание товара'
    )
    price = models.IntegerField(
        verbose_name='Цена Товара'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создание'
    )
    size = models.CharField(
        max_length=55,
        verbose_name='Размер'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Актив'
    )
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Фото продукта'
    )

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продукта'

class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.user} {self.product}"

class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.user)

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.cart)

    class Meta:
        unique_together = ("cart", "product")
    

class OrderStatus(models.TextChoices):
    NEW = "new", "new"
    CONFIRMED = "confirmed", "confirmed"
    canceled = "canceled", "canceled"
    on_way = "on_way", "on_way"
    DELIVERED = "delivered", "delivered"

class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="orders"
    )
    status = models.CharField(
        max_length=20, 
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )
    manager_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="manager_orders"
    )
    courier = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="courier_orders"
    )
    address = models.CharField(
        max_length=155,
        verbose_name='Адрес'
    )
    phone = models.CharField(
        max_length=30,
        verbose_name='Номер телефона'
    )
    comment = models.TextField(
        verbose_name='Коммент'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создание'
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT
    )
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кол-ВО") 

    class Meta:
        unique_together = ("order", "product")
