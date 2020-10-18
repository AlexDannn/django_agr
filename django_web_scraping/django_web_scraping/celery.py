from __future__ import absolute_import
import os
from celery import Celery

from celery.schedules import crontab

# default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_web_scraping.settings')

app = Celery('django_web_scraping')

app.conf.timezone = 'UTC'

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scraping-task-one-min-1': {
        'task': 'scraping.tasks.sports_rss',
        'schedule': crontab(),
    },
    'scraping-task-one-min-2': {
        'task': 'scraping.tasks.hackernews_rss',
        'schedule': crontab(),
    },
    'scraping-task-one-min-3': {
        'task': 'scraping.tasks.games_rss',
        'schedule': crontab(),
    },
    'scraping-task-one-min-4': {
        'task': 'scraping.tasks.movies_rss',
        'schedule': crontab(),
    },
}
