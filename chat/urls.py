from django.urls import path
from chat.api.views import GroupMessagesAPIView

urlpatterns = [
    path('api/groups/<int:group_id>/messages/', GroupMessagesAPIView.as_view(), name='group_messages_api'),
]