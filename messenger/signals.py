from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from messenger.models import Archive, Profile

@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    """ Create a profile for every new user """
    if created:
        Profile.objects.create(owner=instance)

@receiver(pre_delete, sender=User)
def remove_user_from_thread(sender, instance, **kwargs):
    """ Removes participation when user leaves the system """
    for board in instance.message_threads.all():
        board.participants.remove(instance)

@receiver(pre_delete, sender=Archive)
def delete_archive_file(sender, instance, **kwargs):
    """ Removes the archive file on record delete """
    if instance.archive_file:
        instance.archive_file.delete()