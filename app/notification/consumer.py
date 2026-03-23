from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
    # connect - чтобы определять что клиент вошел 
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return
        # тут мы говорим что если клиент анонимный, то возвращаем пустой ответ

        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        # а тут если авторизован то пропускаем 

        await self.accept()

    async def disconnect(self, close_code):
    # disconnect - это чтобы определить что клиент вышел
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async  def send_notification(self, event):
        await self.send_json(event["data"])
    #  тут говорится какое событие (уведомление) json отправляем