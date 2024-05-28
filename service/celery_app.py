import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

app = Celery('service')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

@app.task() # первый таск
def debug_task(): # чтобы использовать: debug_task() или debug_task.delay()
    time.sleep(10)
    print('hello celery from debug_task')
