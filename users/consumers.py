import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Group, Message
from channels.db import database_sync_to_async
from datetime import datetime
from django.shortcuts import get_object_or_404
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
        message = text_data_json.get('message', None)
        file_url = text_data_json.get('file_url', None)
        user = self.scope["user"]
        
        # Oturum açmamış kullanıcıları kontrol et
        if not user.is_authenticated:
            print("Oturum açmamış kullanıcıdan mesaj alındı. Veritabanına kaydedilmeyecek.")
            return

        try:
            group = await database_sync_to_async(Group.objects.get)(id=self.group_id)
            # Eğer mesaj varsa kaydet
            if message or file_url:
                new_message = await database_sync_to_async(Message.objects.create)(
                    sender=user,
                    group=group,
                    content=message,
                    file=file_url,  # Dosya URL'si varsa kaydet
                    id_bilgisi = get_object_or_404(User, username=user).id  # Kullanıcı bilgilerini al
                )
                timestamp = new_message.timestamp.isoformat()
            else:
                timestamp = datetime.now().isoformat()
        except Exception as e:
            print(f"Veritabanına mesaj kaydedilemedi: {e}")
            timestamp = datetime.now().isoformat()

        # Mesajı grup içinde yayınla
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'file_url': file_url,
                'username': user.username,
                'timestamp': timestamp,
                "id_bilgisi": user.id,
                  "last_name": user.last_name,  # Kullanıcı bilgilerini al
                    "profile_picture": user.image.url if user.image else None,
            }
        )

    async def chat_message(self, event):
        message = event.get('message', None)
        file_url = event.get('file_url', None)
        username = event['username']
        timestamp = event['timestamp']
        id = event['id_bilgisi']
        last_name = event['last_name']
        profile_picture = event.get('profile_picture', None)
        # Mesajı WebSocket'ten gönder
        await self.send(text_data=json.dumps({
            'message': message,
            'file_url': file_url,
            'user': username,
            'timestamp': timestamp,
            'id_bilgisi': id ,
            "last_name":last_name,
             "profile_picture":profile_picture# Kullanıcı bilgilerini al
            
        }))