from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MessageManager(models.Manager):
	
	def add_message(self,sender, thread, content):
		return self.create(sender=sender, thread=thread, content=content)
	
	def getMessagebyThread(self,thread):
		return self.filter(thread=thread)

class MessageThread(models.Model):
    subject = models.CharField(max_length=255, blank=True)
    participants = models.ManyToManyField(User, related_name='message_threads')
    when_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return (' {} '.format(self.subject))


class Message(models.Model):
	sender = models.ForeignKey(User, related_name='sender')
	thread = models.ForeignKey(MessageThread, related_name='thread')
	content = models.TextField()
	when_created = models.DateTimeField(auto_now_add=True)

	objects = MessageManager()

	def __str__(self):
		return ('{}:{} '.format(self.thread, self.content))

class Profile(models.Model):
	first_name = models.CharField(max_length=30, blank = False)
	last_name = models.CharField(max_length=30, blank = False)
	owner = models.OneToOneField(User, related_name='owner')
	thread = models.ManyToManyField(MessageThread, 
		related_name = '_thread', through = 'ProfileThread')

	def __str__(self):
		return ('{} : {}  '.format(self.owner, self.thread.count()))

@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    """ Create a profile for every new user """
    if created:
        Profile.objects.create(owner=instance)


class ProfileThread(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
	is_removed = models.BooleanField()
