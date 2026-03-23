import json 

# тут соединение с вебсокетом 

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from app.chat.models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"chat_{self.chat_id}"
# scope - это 
        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return

        is_participant = await self._is_participant()
        if not is_participant:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "type" : "connection_established",
                    "chat_id" : int(self.chat_id),
                    "user_id" : self.user.id,   
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            await self.send_error("Error empty payload")
            return

        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_error("invalid json")
            return

        text = (payload.get("text") or "").strip()
        if not text:
            await self.send_error("text not null")

            return

        message_data = await self._create_message(text)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type" : "chat.message",
                "message" : message_data
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def send_error(self, message):
        await self.send(
            text_data=json.dumps(
                {
                    "type" : "error",
                    "detail" : message
                }
            )
        )

    @sync_to_async
    def _is_participant(self):
        return ChatRoom.objects.filter(id=self.chat_id, participants=self.user).exists()

    @sync_to_async
    def _create_message(self, text):
        message = Message.objects.create(
            chat_id=self.chat_id,
            sender=self.user,
            text=text
        )
        return {
            "type" : "chat_message",
            "id" : message.id,
            "chat_id" : int(self.chat_id),
            "text" : message.text,
            "created_at" : message.created_at.isoformat(),
            "sender" : {
                "id" : self.user.id,
                "email" : self.user.email,
                "first_name" : self.user.first_name, 
                "last_name" : self.user.last_name, 
            }
        }