from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    """
    Authentification JWT personnalisée.
    Permet d'ajouter une logique de validation utilisateur supplémentaire si nécessaire.
    """

    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            return None

        user, validated_token = user_auth_tuple

        # Vérifie si l'utilisateur est actif
        if not user.is_active:
            raise AuthenticationFailed("Utilisateur inactif ou supprimé.", code="user_inactive")

        return user, validated_token
