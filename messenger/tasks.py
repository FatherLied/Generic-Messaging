from datetime import timedelta
from celery.decorators import periodic_task


@periodic_task(run_every=timedelta(seconds=5))
def greet():
    print('Hello')
    print('World')
