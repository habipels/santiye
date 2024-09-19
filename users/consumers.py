# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Group, Message
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = int(self.scope['url_route']['kwargs']['group_id'])
        self.room_group_name = f'chat_{self.group_id}'

        # Odaya katıl
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Odayı terk et
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        # Oturum açmamış kullanıcıları kontrol et
        if not user.is_authenticated:
            print("Oturum açmamış kullanıcıdan mesaj alındı. Veritabanına kaydedilmeyecek.")
            return

        try:
            group = await database_sync_to_async(Group.objects.get)(id=self.group_id)
            await database_sync_to_async(Message.objects.create)(
                sender=user,
                group=group,
                content=message
            )
        except Exception as e:
            print(f"Veritabanına mesaj kaydedilemedi: {e}")

        # Mesajı grup içinde yayınla
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Mesajı WebSocket'ten gönder
        await self.send(text_data=json.dumps({
            'message': message,
            'user': username,
        }))
