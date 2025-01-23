# chat/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:group_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/user_status/', consumers.UserStatusConsumer.as_asgi()),
]
