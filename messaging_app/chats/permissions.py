from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated  # ✅ Auth check

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method in ["PUT", "PATCH", "DELETE"]:  # ✅ méthode check
            return request.user in obj.participants.all()  # ✅ participant check
        return False
