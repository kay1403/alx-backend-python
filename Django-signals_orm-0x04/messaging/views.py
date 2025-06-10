from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Message
from .forms import MessageReplyForm

@login_required
def threaded_conversation_view(request, message_id):
    # Récupération optimisée du message racine
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message'),
        id=message_id
    )

    # Vérification de permission : seul l'expéditeur ou le destinataire peut voir la conversation
    if request.user != message.sender and request.user != message.receiver:
        return HttpResponseForbidden("Vous n'avez pas la permission de voir cette conversation.")

    # Récupération du thread complet avec optimisation (récursif)
    def get_thread_recursive(msg):
        replies = Message.objects.filter(parent_message=msg).select_related('sender', 'receiver').prefetch_related('replies')
        thread = []
        for reply in replies:
            thread.append({
                'message': reply,
                'replies': get_thread_recursive(reply)
            })
        return thread

    thread = get_thread_recursive(message)

    # Traitement du formulaire de réponse
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
