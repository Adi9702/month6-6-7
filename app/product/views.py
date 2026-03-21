from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from app.users.permissions import IsManager, IsCourier, IsCustomer
from app.product.models import Order, OrderStatus, Product, Favorite, Cart, CartItem
from app.product.services import set_order_status
from app.product.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    FavoriteSerializer,
    CartItemSerializer, 
    CartSerializer,
    OrderCreateSerializer
)
from app.pagination import CustomPageNumberPagination
from app.filters import ProductFilter


class ProductViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.select_related("category", "model").prefetch_related("images").order_by("-created_at")
    
    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [AllowAny()]

class FavoriteVIewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request):
        cart = self.get_cart(request.user)
        product_id  = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response({"detail" : "Товар добавлен в корзину"})

    def destroy(self, request, pk=None):
        cart = self.get_cart(request.user)
        item = cart.items.filter(id=pk).first()

        if item:
            item.delete()
            return Response({"detail" : "Удалено"})
        return Response({"detail" : "Not Found"}, status=404)

class OrderViewSet(mixins.CreateModelMixin, 
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet
    ):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderCreateSerializer

    def get_queryset(self):
        user = self.request.user

        if getattr(user, "is_manager", False):
            return Order.objects.all().order_by("-id")

        if getattr(user, "is_courier", False):
            return Order.objects.filter(courier=user).order_by("-id")

        return Order.objects.filter(user=user).order_by("-id")


class OrderStatusUpdateAPI(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk: int):
        order = get_object_or_404(Order, pk=pk)

        new_status = request.data.get("status")
        if not new_status:
            return Response({"detail" : "status invalid"}, status=status.HTTP_400_BAD_REQUEST)

        valid_statuses = {choice for choice, _ in OrderStatus.choices}
        if new_status not in valid_statuses:
            return Response({"detail": "unknown status"}, status=status.HTTP_400_BAD_REQUEST)

        set_order_status(order=order, new_status=new_status, actor=request.user)
        return Response({"ok": True}, status=status.HTTP_200_OK)
