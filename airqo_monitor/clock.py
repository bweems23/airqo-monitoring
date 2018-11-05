from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

# from airqo_monitor.models import ChannelNote
# from airqo_monitor.get_malfunctions import (
#     get_all_channel_malfunctions
# )

from django.core import management

sched = BlockingScheduler()


@sched.scheduled_job('cron', minute=5)
def update_channel_data():
    management.call_command('run_scheduler')
    # print('HI')
    # ChannelNote.objects.create(channel_id=2, note='test note', author='rachel')
    # get_all_channel_malfunctions()

sched.start()

