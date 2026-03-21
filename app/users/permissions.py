from rest_framework.permissions import BasePermission

from app.users.models import UserRole

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_superuser or request.user.role == UserRole.MANAGER
            )
        )

class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (
            request.user.role == UserRole.COURIER
        ))

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and(
            request.user.role == UserRole.CUSTOMER
        ))