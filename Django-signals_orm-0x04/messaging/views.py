from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import logout
from .models import Message
from .forms import MessageReplyForm

@login_required
def threaded_conversation_view(request, message_id):
    # Récupération du message racine avec optimisation des jointures
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message')
                       .prefetch_related('replies__sender', 'replies__receiver'),
        id=message_id
    )

    # Vérification d'autorisation
    if request.user != message.sender and request.user != message.receiver:
        return HttpResponseForbidden("Vous n'avez pas la permission de voir cette conversation.")

    # Construction récursive du thread
    def get_thread(msg):
        replies = Message.objects.filter(parent_message=msg).select_related('sender', 'receiver')
        thread = []
        for reply in replies:
            thread.append({
                'message': reply,
                'replies': get_thread(reply)
            })
        return thread

    thread = get_thread(message)

    # Gestion du formulaire de réponse
    if request.method == 'POST':
        form = MessageReplyForm(request.POST)
        if form.is_valid():
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


@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Votre compte a été supprimé avec succès.")
        return redirect('home')
    return render(request, 'messaging/delete_user_confirm.html')
