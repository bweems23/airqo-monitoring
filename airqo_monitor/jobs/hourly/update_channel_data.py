from django_extensions.management.jobs import HourlyJob

from airqo_monitor.get_malfunctions import (
    get_all_channel_malfunctions
)


class Job(HourlyJob):
    help = "My sample job."

    def execute(self):
        # executing empty sample job
        print("YO")
        get_all_channel_malfunctions()
