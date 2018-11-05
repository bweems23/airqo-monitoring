from django.core.management.base import BaseCommand, CommandError

from airqo_monitor.models import ChannelNote
from airqo_monitor.get_malfunctions import (
    get_all_channel_malfunctions
)

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


class Command(BaseCommand):
    help = 'Runs all scheduler tasks'

    def handle(self, *args, **options):
        print('Running scheduled tasks...')
        get_all_channel_malfunctions()
        print('Scheduled tasks complete.')
