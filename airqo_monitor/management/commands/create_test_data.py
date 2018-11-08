import json

from django.core.management.base import BaseCommand, CommandError

from airqo_monitor.management.commands.utils import create_basic_test_data


class Command(BaseCommand):
    help = 'Creates test data necessary for local development. This deletes your existing local data.'

    def handle(self, *args, **options):
        create_basic_test_data()
