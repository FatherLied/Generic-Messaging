from django.utils import timezone

from datetime import timedelta
from itertools import chain
from celery.decorators import periodic_task
from messenger.models import Archive
from messenger.utils import publish_to_csv
# from datetime import datetime


# @periodic_task(run_every=timedelta(seconds=5))
# def greet():
#     print('Hello')
#     print('World')

@periodic_task(run_every=timedelta(seconds=10))
def check_archive_queue():
    """Processes requests to archive thread"""
    archives = Archive.objects.filter(status='Q')[:5] # Filter all pending archives; processing 5 at a time
    processed = []
    for archive in archives:
        if archive.status is 'Q':
            archive.status = 'P'
            archive.save()

            try:
                # archive.save_file(publish_to_csv(archive.thread))
                archive.archive_file = publish_to_csv(archive.thread)
            except Exception:
                print('Something went wrong')
                archive.status is 'Q'
            else:
                archive.status = 'F'
                processed.append(archive)
            
        archive.save()
        # [1] update status here so that the next `check_archive_queue`  call
        # won't process the already processed archive
        # [2] run the actual archiving of thread
        # [3] save reference of `archive_path` to archive instance
        # [4] append `archive` instance to processed

    # :o so tasks return something?
    # not necessarily but when you use monitoring tools such as 'Celery Flower'
    # it's nice to see what instances are actually processed
    # Yes, this is possible since AMQP allows other components to send messages
    # not just the brokers; in this case, workers as well
    print('\n')

    for record in processed:
        print('{}\n'.format(record))

    print('\n')

    return processed


@periodic_task(run_every=timedelta(minutes=1))
def check_expired_archive():
    """Deletes archive model instances and files that are expired"""
    expired_archives = Archive.objects.filter(status='E')
    deleted = []

    # Archives without requestors
    vagrant_archives = Archive.objects.filter(requestor=None)

    trash_archives = list(chain(expired_archives, vagrant_archives))

    for archive in trash_archives:
        deleted.append(archive)

        archive.archive_file.delete()
        archive.delete()
        # archive.save()

    return deleted

@periodic_task(run_every=timedelta(minutes=1))
def expire_archives():
    """Expires unclaimed archives"""
    unused_archives = Archive.objects.filter(status='F')
    expired = []

    for archive in unused_archives:
        current_time = timezone.now()

        if current_time > archive.expiry:
            archive.status = 'E'
            archive.save()

            expired.append(archive)

    return expired