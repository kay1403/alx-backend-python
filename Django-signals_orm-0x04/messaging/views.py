# messaging/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Message
from .forms import MessageReplyForm  # à créer pour saisir la réponse

@login_required
def threaded_conversation_view(request, message_id):
    # Récupération du message racine avec optimisation FK
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message'),
        id=message_id
    )

    # Vérification d'autorisation simple : 
    # seul l'expéditeur ou le destinataire peut voir ce thread
    if request.user != message.sender and request.user != message.receiver:
        return HttpResponseForbidden("Vous n'avez pas la permission de voir cette conversation.")

    # Construction du thread récursif
    thread = message.get_thread()

    if request.method == 'POST':
        form = MessageReplyForm(request.POST)
        if form.is_valid():
            # Création de la réponse
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.receiver = message.sender if message.sender != request.user else message.receiver
            reply.parent_message = message
            reply.save()
            messages.success(request, "Votre réponse a été envoyée avec succès.")
            return redirect('threaded_conversation', message_id=message_id)
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
