import os
from celery.schedules import crontab
from celery import Celery
from test_app import views

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_board.settings')

app = Celery('message_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'task': 'test_app.views.my_task',
    },
}

