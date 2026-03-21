import asyncio
import json

from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from app.chat.models import ChatRoom, Message
from app.users.models import User
from core.asgi import application


async def ws_connect(communicator: WebsocketCommunicator, timeout: int = 5):
    await communicator.send_input({"type": "websocket.connect"})
    # Give the application task a chance to start and handle the connect event.
    await asyncio.sleep(0.05)
    response = await communicator.receive_output(timeout=timeout)
    if response["type"] == "websocket.close":
        return False, response.get("code", 1000)
    return True, response.get("subprotocol", None)


class ChatWebsocketTests(TransactionTestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="u1@example.com",
            password="password123",
            first_name="U1",
            last_name="Test",
        )
        self.user2 = User.objects.create_user(
            email="u2@example.com",
            password="password123",
            first_name="U2",
            last_name="Test",
        )

        self.room = ChatRoom.objects.create(title="Room", created_by=self.user1)
        self.room.participants.set([self.user1, self.user2])

    def _ws_path(self, chat_id: int, token: str | None = None) -> str:
        path = f"/ws/chat/rooms/{chat_id}/"
        if token:
            path += f"?token={token}"
        return path

    def test_connect_requires_auth(self):
        async def inner():
            communicator = WebsocketCommunicator(application, self._ws_path(self.room.id))
            connected, close_code = await ws_connect(communicator, timeout=5)
            self.assertFalse(connected)
            self.assertEqual(close_code, 4001)

        asyncio.run(inner())

    def test_connect_requires_participant(self):
        outsider = User.objects.create_user(
            email="outsider@example.com",
            password="password123",
            first_name="Out",
            last_name="Sider",
        )
        token = str(AccessToken.for_user(outsider))

        async def inner():
            communicator = WebsocketCommunicator(application, self._ws_path(self.room.id, token))
            connected, close_code = await ws_connect(communicator, timeout=5)
            self.assertFalse(connected)
            self.assertEqual(close_code, 4003)

        asyncio.run(inner())

    def test_connect_and_send_message(self):
        token = str(AccessToken.for_user(self.user1))

        async def inner():
            communicator = WebsocketCommunicator(application, self._ws_path(self.room.id, token))
            connected, _ = await ws_connect(communicator, timeout=5)
            self.assertTrue(connected)

            raw = await communicator.receive_from(timeout=5)
            hello = json.loads(raw)
            self.assertEqual(hello["type"], "connection_established")
            self.assertEqual(hello["chat_id"], self.room.id)
            self.assertEqual(hello["user_id"], self.user1.id)

            await communicator.send_to(text_data="not-json")
            raw = await communicator.receive_from(timeout=5)
            err = json.loads(raw)
            self.assertEqual(err["type"], "error")

            await communicator.send_to(text_data=json.dumps({"text": ""}))
            raw = await communicator.receive_from(timeout=5)
            err = json.loads(raw)
            self.assertEqual(err["type"], "error")

            await communicator.send_to(text_data=json.dumps({"text": "hi"}))
            raw = await communicator.receive_from(timeout=5)
            msg = json.loads(raw)
            self.assertEqual(msg["type"], "chat_message")
            self.assertEqual(msg["chat_id"], self.room.id)
            self.assertEqual(msg["text"], "hi")
            self.assertEqual(msg["sender"]["id"], self.user1.id)

            await communicator.disconnect()

        asyncio.run(inner())

        self.assertEqual(Message.objects.filter(chat=self.room).count(), 1)
        message = Message.objects.get(chat=self.room)
        self.assertEqual(message.sender_id, self.user1.id)
        self.assertEqual(message.text, "hi")
