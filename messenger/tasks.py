from datetime import timedelta
from celery.decorators import periodic_task
from messenger.models import Archive


@periodic_task(run_every=timedelta(seconds=5))
def greet():
    print('Hello')
    print('World')

@periodic_task(run_every=timedelta(minutes=1))
def check_archive_queue():
    """Processes requests to archive thread"""
    archives = Archive.objects.filter()[:5] # Filter all pending archives; processing 5 at a time
    processed = []
    for archive in archives:
        if archive.status is 'Q':
            archive.status = 'P'

            
        # [1] update status here so that the next `check_archive_queue`  call
        # won't process the already processed archive
        # [2] run the actual archiving of thread
        # [3] save reference of `archive_path` to archive instance
        # [4] append `archive` instance to processed
        pass
    # :o so tasks return something?
    # not necessarily but when you use monitoring tools such as 'Celery Flower'
    # it's nice to see what instances are actually processed
    # Yes, this is possible since AMQP allows other components to send messages
    # not just the brokers; in this case, workers as well
    return processed


@periodic_task(run_every=timedelta(minutes=30))
def check_expired_archive():
    """Deletes archive model instances and files that are expired"""
    expired_archives = Archive.filter(status='D')

    for archive in expired_archives:
        archive.remove()

    pass