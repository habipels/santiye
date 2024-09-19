# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Group, Message
from channels.db import database_sync_to_async
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Room'a katıl
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Room'dan çık
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]  # Oturum açmış kullanıcıyı al

        try:
            # Mesajı veritabanına kaydet
            group = await database_sync_to_async(Group.objects.get)(name=self.room_name)
            await database_sync_to_async(Message.objects.create)(
                sender=user,  # 'user' değişkeni, oturum açmış kullanıcıyı temsil etmeli
                group=group,  # Mesajın gönderileceği grup
                content=message  # Mesaj içeriği
            )
        except Exception as e:
            print(f"Veritabanına mesaj kaydedilemedi: {e}")

        

        # Mesajı grup içinde yayınla
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Mesajı WebSocket'ten gönder
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))
