from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def track_message_edits(sender, instance, **kwargs):
    if not instance.pk:
        return  # Nouveau message → pas besoin d'historique

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Si le contenu change
    if old_instance.content != instance.content:
        # Enregistrer l'ancienne version
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content,
            edited_by=instance.edited_by  # doit être défini dans la vue
        )
        # Marquer comme édité
        instance.edited = True
