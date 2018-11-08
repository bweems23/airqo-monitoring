from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand, CommandError

from airqo_monitor.malfunction_detection.get_malfunctions import get_all_channel_malfunctions


class Command(BaseCommand):
    help = 'Runs all scheduler tasks'

    def handle(self, *args, **options):
        sched = BlockingScheduler()

        @sched.scheduled_job('cron', hour='*')
        def update_channel_data():
            print('Running scheduled tasks...')
            get_all_channel_malfunctions()
            print('Scheduled tasks complete.')

        sched.start()
