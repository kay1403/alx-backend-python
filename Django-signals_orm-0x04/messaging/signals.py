from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    # Supprimer les messages envoyés ou reçus
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Supprimer les notifications liées
    Notification.objects.filter(user=instance).delete()

    # Supprimer l'historique des messages liés
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        # Crée une notification pour le destinataire
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit_history(sender, instance, **kwargs):
    if not instance.pk:
        # Nouveau message, rien à faire ici
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Si le contenu a changé, sauvegarder l'historique
    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_instance.content,
            edited_by=instance.edited_by
        )
        # Mettre à jour les champs d'édition du message
        instance.edited = True
        from django.utils import timezone
        instance.edited_at = timezone.now()
