from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Message, MessageHistory
from .serializers import MessageHistorySerializer

# Vue HTML pour afficher l'historique dans une page web
@login_required
def message_history_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')

    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })

# Vue API DRF pour afficher l'historique en JSON
class MessageHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
        serializer = MessageHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
