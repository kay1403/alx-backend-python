from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager  # Manager personnalisé

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # Champ pour message lu/non lu

    # Champs pour suivi édition
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')

    objects = models.Manager()  # Manager par défaut
    unread = UnreadMessagesManager()  # Manager custom pour messages non lus

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'

    def get_thread(self):
        """
        Récupère récursivement ce message et toutes ses réponses en structure arborescente.
        """
        thread = {
            'message': self,
            'replies': []
        }
        replies_qs = self.replies.select_related('sender', 'receiver').order_by('timestamp')
        for reply in replies_qs:
            thread['replies'].append(reply.get_thread())
        return thread

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} about message {self.message.id}'

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Edit history of message {self.message.id} at {self.edited_at}'
