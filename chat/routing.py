from django.urls import path
from chat.consumers import GroupChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:group_id>/', GroupChatConsumer.as_asgi()),
]
