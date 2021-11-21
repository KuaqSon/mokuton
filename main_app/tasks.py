import time

from huey import crontab
from huey.contrib.djhuey import task, periodic_task, db_task

# https://huey.readthedocs.io/en/latest/guide.html

def tprint(s, c=32):
    # Helper to print messages from within tasks using color, to make them
    # stand out in examples.
    print('\x1b[1;%sm%s\x1b[0m' % (c, s))


# Periodic tasks.

@periodic_task(crontab(minute='*/1'))
def every_other_minute():
    tprint('This task runs every 1 minutes.', 35)
