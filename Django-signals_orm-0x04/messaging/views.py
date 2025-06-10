from django.shortcuts import render, get_object_or_404
from .models import Message, MessageHistory

def message_history_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')

    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })
