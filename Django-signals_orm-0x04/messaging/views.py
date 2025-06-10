from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page

from .models import Message
from .forms import MessageReplyForm

@login_required
@cache_page(60)  # Cache 60 secondes la vue
def threaded_conversation_view(request, message_id):
    # Récupération optimisée du message racine
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message').only(
            'id', 'sender_id', 'receiver_id', 'content', 'timestamp', 'parent_message_id', 'edited', 'read'
        ),
        id=message_id
    )

    if request.user != message.sender and request.user != message.receiver:
        return HttpResponseForbidden("Vous n'avez pas la permission de voir cette conversation.")

    def get_thread_recursive(msg):
        replies = Message.objects.filter(parent_message=msg).select_related('sender', 'receiver').only(
            'id', 'sender_id', 'receiver_id', 'content', 'timestamp', 'parent_message_id', 'edited', 'read'
        ).order_by('timestamp')
        thread = []
        for reply in replies:
            thread.append({
                'message': reply,
                'replies': get_thread_recursive(reply)
            })
        return thread

    thread = get_thread_recursive(message)

    if request.method == 'POST':
        form = MessageReplyForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            receiver = message.sender if message.sender != request.user else message.receiver
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                parent_message=message,
                content=content
            )
            messages.success(request, "Votre réponse a été envoyée avec succès.")
            return redirect('threaded_conversation', message_id=message.id)
        else:
            messages.error(request, "Erreur dans le formulaire, veuillez corriger.")
    else:
        form = MessageReplyForm()

    context = {
        'message': message,
        'thread': thread,
        'form': form,
    }
    return render(request, 'messaging/threaded_conversation.html', context)


@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender_id', 'receiver_id', 'content', 'timestamp', 'parent_message_id', 'edited', 'read'
    )
    return render(request, 'messaging/unread_messages.html', {
        'messages': unread_messages
    })


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Déconnecte l'utilisateur avant suppression
    user.delete()
    return redirect('home')  # Change 'home' par la route souhaitée après suppression
