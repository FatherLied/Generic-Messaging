from django.contrib.auth.models import User
from .models import WidgetThread, WidgetMessage
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

class WidgetThreadModelTestCase(TestCase):
    """ Tests for MessageThread model """
    def test_thread_when(self):
        """Test the field `when`"""
        self.assertEqual(WidgetThread.objects.count(), 0)
        tomorrow = timezone.now() + timedelta(days=1)
        self.assertEqual(WidgetThread.objects.filter(when__gte=tomorrow).count(), 0)

    def setUp(self):
        self.user1 = User.objects.create_user(username='User1', password='pass')


    def test_thread_create(self):
        """Test creating a thread with subject and participants"""
        self.assertEqual(WidgetThread.objects.count(), 0)
        self.assertEqual(self.user1.message_threads.count(), 0)

        WidgetThread.objects.create()
        self.assertEqual(WidgetThread.objects.count(), 1)
        self.assertEqual(self.user1.message_threads.count(), 1)

    def test_message_create(self):
        """Test creating of message. Find a way to refer `sender`, `content`, `when`"""
        
        thread1 = WidgetThread.objects.create()

        thread1.participants.add(self.user1)


        self.assertEqual(self.user1.message_threads.count(), 1)

        WidgetMessage.objects.add_message(sender=self.user1, 
            content="Guys, let's eat!", thread=thread1)
        
        self.assertEqual(WidgetMessage.objects.count(), 1)
        
        
        WidgetMessage.objects.add_message(sender=self.user1, 
            content='Alright!', thread=thread1)
        
        self.assertEqual(WidgetMessage.objects.count(), 2)