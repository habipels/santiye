import json
import socket
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Group, Message, DeviceToken
from channels.db import database_sync_to_async
from datetime import datetime
from .firebase import send_fcm_notification
from asgiref.sync import sync_to_async

User = get_user_model()

def send_message_to_user(user_id, message, host="127.0.0.1", port=9001):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(message.encode())
        sock.close()
        print(f"[TCP] TCP ile user_id {user_id} -> mesaj: {message}")
    except Exception as e:
        print(f"[TCP ERROR] {user_id}: {e}")

def get_group_members_excluding_sender(group, sender_user):
    return list(group.members.exclude(id=sender_user.id).all())

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = int(self.scope['url_route']['kwargs']['group_id'])
        self.room_group_name = f'chat_{self.group_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        file_url = text_data_json.get('file_url')
        user = self.scope["user"]

        try:
            group = await database_sync_to_async(Group.objects.get)(id=self.group_id)
            if message or file_url:
                new_message = await database_sync_to_async(Message.objects.create)(
                    sender=user,
                    group=group,
                    content=message,
                    file=file_url,
                )
                timestamp = new_message.timestamp.isoformat()
                await self.send_fcm_to_group_members(group, user, message or "Yeni bir dosya gönderildi")
            else:
                timestamp = datetime.now().isoformat()
        except Exception as e:
            print(f"Veritabanına mesaj kaydedilemedi: {e}")
            timestamp = datetime.now().isoformat()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'file_url': file_url,
                'username': user.username,
                'timestamp': timestamp,
                "id_bilgisi": user.id,
                "last_name": user.last_name,
                "profile_picture": user.image.url if hasattr(user, 'image') and user.image else None,
            }
        )
        await self.channel_layer.group_send(
            "global_chat",
            {
                "type": "global_message",
                "content": f"{user.username} tarafından bir gruba mesaj gönderildi",
                "group_id": self.group_id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event.get('message'),
            'file_url': event.get('file_url'),
            'user': event['username'],
            'timestamp': event['timestamp'],
            'id_bilgisi': event['id_bilgisi'],
            "last_name": event['last_name'],
            "profile_picture": event.get('profile_picture'),
        }))

    async def send_fcm_to_group_members(self, group, sender_user, content):
        print(f"[FCM] Grup üyelerine bildirim gönderiliyor: {group.name} - {sender_user.username}")
        members = await database_sync_to_async(get_group_members_excluding_sender)(group, sender_user)

        for member in members:
            print(f"[Bildirim] Üye: {member.username}")
            try:
                token_obj = await database_sync_to_async(DeviceToken.objects.filter(user=member).first)()
                if token_obj and token_obj.token:
                    platform = token_obj.platform.lower()  # "web", "android" veya "ios"

                    if platform == "web":
                        url = f"https://seninsite.com/chat/{group.id}/"
                        data_payload = {
                            "platform": platform,
                            "url": url,
                            "group_id": str(group.id)
                        }
                    elif platform in ["android", "ios"]:
                        data_payload = {
                            "platform": platform,
                            "screen": "ChatScreen",
                            "group_id": str(group.id)
                        }
                    else:
                        data_payload = {
                            "platform": platform,
                            "group_id": str(group.id)
                        }

                    response = await sync_to_async(send_fcm_notification)(
                        token=token_obj.token,
                        title=sender_user.get_full_name() or sender_user.username,
                        body=content,
                        platform=platform,
                        url=data_payload.get("url"),
                        screen=data_payload.get("screen"),
                        extra_data={"group_id": data_payload.get("group_id")}
                    )
                    await self.send(text_data=json.dumps({
                        "type": "fcm_status",
                        "to_user": member.username,
                        "fcm_response": response or "Gönderilemedi"
                    }))
            except Exception as e:
                await self.send(text_data=json.dumps({
                    "type": "fcm_status",
                    "to_user": member.username,
                    "fcm_response": f"Hata: {str(e)}"
                }))

            try:
                await sync_to_async(send_message_to_user)(
                    user_id=member.id,
                    message=f"Mesaj geldi - Grup: {group.id} - İçerik: {content}"
                )
            except Exception as e:
                print(f"[TCP Bildirim Hatası] {member.id}: {e}")

class GlobalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("global_chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("global_chat", self.channel_name)

    async def global_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "global_message",
            "content": event["content"],
            "group_id": event.get("group_id")
        }))
