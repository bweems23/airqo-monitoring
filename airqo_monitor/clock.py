# import django

# from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler

from airqo_monitor.models import ChannelNote
from airqo_monitor.get_malfunctions import (
    get_all_channel_malfunctions
)

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")


# settings.configure()
# django.setup()
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def update_channel_data_interval():
    print('HI')
    ChannelNote.objects.create(channel_id=2, note='test note INTERVAL', author='rachel')
    get_all_channel_malfunctions()

@sched.scheduled_job('cron', minute=5)
def update_channel_data():
    print('HI')
    ChannelNote.objects.create(channel_id=2, note='test note', author='rachel')
    get_all_channel_malfunctions()

sched.start()
# import time

# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")

# @register_job(scheduler, "interval", minutes=1)
# def test_job():
#     print("I'm a test job!")
#     # raise ValueError("Olala!")

# register_events(scheduler)

# scheduler.start()
# print("Scheduler started!")
