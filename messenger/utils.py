# from .models import MessageThread, Message
from pathlib import Path
import os

"""
Returns filename on use.

Please store on call 
    i.e. 'messenger.models.Archive.reference = publish_to_csv(thread)'

    Note: Ensure that Archive does not have a reference before calling this else there will betwo files
        with the same content
"""
def publish_to_csv(thread):
    # archive_date = thread.when_created.date()
    folder_path = 'messenger/archived'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # filename = '{}/archive-{}.csv'.format(folder_path,
        # thread.when_created.date().strftime('%Y-%m-%d'))

    filename = 'archive-{}.csv'.format(thread.when_created.date().strftime('%Y-%m-%d'))
    inc = 1

    while Path(os.path.join(folder_path, filename)).exists():
        filename = 'archive-{}[{}].csv'.format(thread.when_created.date().strftime('%Y-%m-%d'), inc)
        inc += 1

    
    with open( os.path.join(folder_path, filename), 'w') as archive:
        thread_content = thread.content.all().order_by('when_created')

        for message in thread_content:
            user = message.sender

            timestamp = message.when_created.strftime('%Y-%m-%d %H:%M:%S')
            user_email = user.email if user.email else 'NO-EMAIL'

            # archive.write('{}: {} \n\t "{}" @{}\n\n'.format(user_email, user.username, message.content, timestamp))
            archive.write('{},{},"{}",{}\n'.format(user_email, user.username, message.content, timestamp))

    return os.path.join(folder_path, filename)
