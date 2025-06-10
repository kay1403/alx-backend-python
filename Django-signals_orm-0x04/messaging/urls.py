from django.urls import path
from .views import message_history_view, MessageHistoryAPIView

urlpatterns = [
    # Vue HTML
    path('messages/<int:message_id>/history/', message_history_view, name='message_history'),

    # API JSON
    path('api/messages/<int:message_id>/history/', MessageHistoryAPIView.as_view(), name='message_history_api'),
]
