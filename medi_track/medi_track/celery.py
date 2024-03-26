# from __future__ import absolute_import, unicode_literals
# import os
# from celery.schedules import crontab
# from celery import Celery
# from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medi_track.settings')

# app = Celery('medi_track')

# # Set to True if you want to work with UTC time
# app.conf.enable_utc = False

# # Set your timezone
# app.conf.update(timezone='Asia/Kolkata')

# # Load Celery configuration from Django settings
# app.config_from_object(settings, namespace='CELERY')

# # Automatically discover tasks in all apps included in the Django project
# app.autodiscover_tasks()

# # Uncomment and configure the beat schedule for periodic tasks
# # app.conf.beat_schedule = {
# #     'send-medicine-time-reminders': {
# #         'task': 'doctor.tasks.send_notification_based_on_times',
# #         'schedule': crontab(minute='*/1'),  # Adjust as needed
# #     },
# # }

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medi_track.settings')

app = Celery('medi_track')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()