from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Authorize list/create for authenticated users
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Accessing a Conversation
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # Accessing a Message
        if isinstance(obj, Message):
            if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                return request.user in obj.conversation.participants.all()

        return False
