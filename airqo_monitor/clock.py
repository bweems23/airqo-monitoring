from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

from airqo_monitor.models import ChannelNote
from airqo_monitor.get_malfunctions import (
    get_all_channel_malfunctions
)


sched = BlockingScheduler()


@sched.scheduled_job('cron', minute=5)
def update_channel_data():
    print('HI')
    ChannelNote.objects.create(channel_id=2, note='test note', author='rachel')
    get_all_channel_malfunctions()

sched.start()

