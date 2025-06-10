# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username='sender', password='pass')
        receiver = User.objects.create_user(username='receiver', password='pass')

        msg = Message.objects.create(sender=sender, receiver=receiver, content='Hello!')
        
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.user, receiver)
        self.assertEqual(notif.message, msg)
