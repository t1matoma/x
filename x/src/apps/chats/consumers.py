import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .services.message_service import MessageService
from .models.chat import Chat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if isinstance(self.scope['user'], AnonymousUser):
            await self.close()
            return
        
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        
        is_member = await self.check_chat_membership()
        if not is_member:
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    @database_sync_to_async
    def check_chat_membership(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return chat.members.filter(id=self.scope['user'].id).exists()
        except Chat.DoesNotExist:
            return False
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            content = data.get('content')
            
            if not content or not content.strip():
                return
            
            message_data = await self.create_message(content)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_data
                }
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    @database_sync_to_async
    def create_message(self, content):
        message = MessageService.send_message(
            user=self.scope["user"],
            content=content,
            chat_id=self.chat_id
        )
        
        return {
            "id": message.id,
            "sender_username": message.sender.username,  
            "content": message.content,
            "timestamp": str(message.timestamp),
        }
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))