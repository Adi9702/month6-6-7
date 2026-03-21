
from rest_framework.routers import DefaultRouter
from django.urls import path

from app.product.views import ProductViewSet, FavoriteVIewSet, CartViewSet, OrderViewSet, OrderStatusUpdateAPI

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("favorites", FavoriteVIewSet, basename="favorites")
router.register("cart", CartViewSet, basename="cart")
router.register("orders", OrderViewSet, basename='order')

urlpatterns = [
    path("change-status/<int:pk>/status", OrderStatusUpdateAPI.as_view(), name='newstatus')
]

urlpatterns += router.urls