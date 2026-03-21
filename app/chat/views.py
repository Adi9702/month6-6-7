from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.chat.authentication import QueryParamJWTAuthentication
from app.chat.models import ChatRoom
from app.chat.serializers import (
    ChatRoomCreateSerializer,
    ChatRoomSerializer
)
# вот тут говорим свагеру про токены (то что такое есть, там после ? пишем токен)
token_parameter = openapi.Parameter(
    "token",
    openapi.IN_QUERY,
    description="JWT access token. Example : ?token=<token>",
    type=openapi.TYPE_STRING,
    required=True    
)

class ChatRoomViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    authentication_classes = [QueryParamJWTAuthentication]

    # вот тут определяется какие чаты может видеть
    def get_queryset(self):
        return (
            ChatRoom.objects.filter(participants=self.request.user)
            # только те чаты, где пользователь участвует
            .prefetch_related("participants", "messages__sender")
            # заранее загружает связанные данные (ускоряет запросы)
            .select_related("created_by")
            # подтягивает создателя
            .distinct()
            # убирает дубликаты
        )
    
    def get_serializer_class(self):
        if self.action == "create":
            return ChatRoomCreateSerializer
        return ChatRoomSerializer

    # тут чтобы получить список чатов
    @swagger_auto_schema(manual_parameters=[token_parameter])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[token_parameter],
        request_body=ChatRoomCreateSerializer,
        responses={201: ChatRoomSerializer},
    )
    # тут создаем чат
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        output_serializer = ChatRoomSerializer(chat, context=self.get_serializer_context())
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(manual_parameters=[token_parameter])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
