from django.urls import path
from .views import (
    message_history_view,
    MessageHistoryAPIView,
    threaded_conversation_view,
)

urlpatterns = [
    # Vue HTML pour l'historique des messages
    path('messages/<int:message_id>/history/', message_history_view, name='message_history'),

    # API JSON pour l'historique des messages
    path('api/messages/<int:message_id>/history/', MessageHistoryAPIView.as_view(), name='message_history_api'),

    # Vue pour la conversation en fil de discussion (threaded)
    path('messages/thread/<int:message_id>/', threaded_conversation_view, name='threaded_conversation'),
]
