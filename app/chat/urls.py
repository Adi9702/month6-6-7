from rest_framework.routers import DefaultRouter
from app.chat.views import ChatRoomViewSet

router = DefaultRouter()
router.register("rooms", ChatRoomViewSet, basename='chat-room')

urlpatterns = router.urls