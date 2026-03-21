from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenBlacklistView
)
from app.users.views import RegisterAPI, ProfileAPI, TelegramLinkCodeView, CustomToken

router = DefaultRouter()
router.register(r"register", RegisterAPI, basename='register')
router.register(r"profile", ProfileAPI, basename='profile')

urlpatterns = [
    path("token/", CustomToken.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", TokenBlacklistView.as_view()),
    path("telegram/", TelegramLinkCodeView.as_view())
]

urlpatterns += router.urls
