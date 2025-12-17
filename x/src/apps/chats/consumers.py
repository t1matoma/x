import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .services.message_service import MessageService

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('content')

        message = await database_sync_to_async(MessageService.send_message)(
            user=self.scope["user"],
            content=content,
            chat_id=self.chat_id
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "id": message.id,
                    "sender": message.sender_id,
                    "content": message.content,
                    "timestamp": str(message.timestamp),
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
