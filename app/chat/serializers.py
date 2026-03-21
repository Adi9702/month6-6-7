from rest_framework import serializers

from app.chat.models import ChatRoom, Message
from app.users.models import User

class ChatUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]

class MessageSerializers(serializers.ModelSerializer):
    sender = ChatUserSerializers(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', "text", "created"]
        read_only_fields = ['id', "sender", "created"]

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = ChatUserSerializers(many=True, read_only=True)
    websocket_url = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ["id", "title", "participants", "created_by", "created", "websocket_url"]

    def get_websocket_url(self, obj):
        return f"/ws/chat/rooms/{obj.id}/"

class ChatRoomCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        write_only=True,
        allow_empty=False
    )

    class Meta:
        model = ChatRoom
        fields = ['id', "title", "participant_ids", "created"]

    def validate_participant_ids(self, value):
        unique_ids = list(dict.fromkeys(value))
        users = User.objects.filter(id__in=unique_ids)

        if users.count() != len(unique_ids):
            raise serializers.ValidationError("Пользователи не найдены")
        
        request_user = self.context["request"].user
        if request_user.id not in unique_ids:
            unique_ids.append(request_user.id)

        if len(unique_ids) < 2:
            raise serializers.ValidationError("В чате должно быть минимум 2 участника")
        
        return unique_ids

    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids")
        request_user = self.context["request"].user

        chat = ChatRoom.objects.create(created_by=request_user, **validated_data)
        chat.participants.set(User.objects.filter(id__in=participant_ids))
        return chat

class MessageCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text']
