from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
from syslab.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syslab.settings')
app = Celery('x', broker=CELERY_BROKER_URL, include=['core.asynctask'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    # 'add-every-30-seconds': {
    #     'task': 'core.asynctask.pushFCM',
    #     'schedule': 30.0,
    # },
    # 'add-every-3600-seconds': {
    #     'task': 'core.asynctask.addTipoPoliza',
    #     'schedule': 3600.0,
    # },
    # 'add-every-10800-seconds': {
    #     'task': 'api.asynctask.getFacturasPDF',
    #     'schedule': 10800.0,
    # },
    # 'add-every-60-seconds': {
    #     'task': 'asegurados.asynctask.sendMailPolizaSiniestro',
    #     'schedule': 60.0,
    # },
    # 'every day between 8 AM"': {
    #     'task': 'asegurados.asynctask.sendNotificacionPolizaVencida',
    #     "schedule": crontab(hour='8',
    #                         minute=0,
    #                         )
    # },
}
#app.conf.timezone = 'UTC'


#@app.task(bind=True)
#def debug_task(self):
#    print('Request: {0!r}'.format(self.request))