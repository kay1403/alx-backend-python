from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Only allow users who are participants of the conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
