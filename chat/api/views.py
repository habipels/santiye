from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat.models import Message
from chat.api.serializers import MessageSerializer

class GroupMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        messages = Message.objects.filter(group_id=group_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
