# chat/routing.py

from django.urls import path,re_path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:group_id>/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/global/$', consumers.GlobalConsumer.as_asgi()),
]