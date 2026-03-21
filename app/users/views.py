from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response

from app.users.models import User, TelegramLinkCode
from app.users.serializers import RegisterSerializers, UserProfileSerializers, TokenObtainPairSerializer

class RegisterAPI(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

class ProfileAPI(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [IsAuthenticated,]

class TelegramLinkCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        obj, _ = TelegramLinkCode.objects.get_or_create(user=request.user)

        obj.code = TelegramLinkCode.generate_code()
        obj.is_user = False
        obj.save(update_fields=["code", "is_user"])

        return Response({"code": obj.code})

class CustomToken(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer