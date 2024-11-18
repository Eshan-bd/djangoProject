# your_project/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('django-tasks')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Schedule tasks
app.conf.beat_schedule = {
    'send-weekly-email': {
        'task': 'your_app.tasks.send_weekly_email_to_users',
        'schedule': crontab(minute='0', hour='0', day_of_week='monday'),  # Run every Monday at midnight
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()