from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand, CommandError

from airqo_monitor.models import ChannelNote
from airqo_monitor.get_malfunctions import get_all_channel_malfunctions


class Command(BaseCommand):
    help = 'Runs all scheduler tasks'

    def handle(self, *args, **options):
        sched = BlockingScheduler()

        @sched.scheduled_job('cron', minute='*')
        def update_channel_data():
            print('Running scheduled tasks...')
            ChannelNote.objects.create(channel_id=2, note='test note clock try', author='rachel')
            get_all_channel_malfunctions()
            print('Scheduled tasks complete.')

        sched.start()
