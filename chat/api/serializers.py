from rest_framework import serializers
from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_name', 'content', 'timestamp', 'file']
