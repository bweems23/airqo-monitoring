from django.core.management.base import BaseCommand, CommandError

from airqo_monitor.models import ChannelNote
from airqo_monitor.get_malfunctions import (
    get_all_channel_malfunctions
)


class Command(BaseCommand):
    help = 'Runs all scheduler tasks'

    def handle(self, *args, **options):
        print('Running scheduled tasks...')
        get_all_channel_malfunctions()
        ChannelNote.objects.create(channel_id=2, note='updated channel malfunctions', author='rachel')
        print('Scheduled tasks complete.')
