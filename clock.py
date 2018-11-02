from apscheduler.schedulers.blocking import BlockingScheduler

from airqo_monitor.get_malfunctions import (
    get_all_channel_malfunctions
)
from airqo_monitor.models import ChannelNote

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def update_channel_data_interval():
    ChannelNote.objects.create(channel_id=2, note='test note INTERVAL', author='rachel')
    get_all_channel_malfunctions()

@sched.scheduled_job('cron', minute=5)
def update_channel_data():
    ChannelNote.objects.create(channel_id=2, note='test note', author='rachel')
    get_all_channel_malfunctions()

sched.start()