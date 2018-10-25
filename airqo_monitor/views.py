from django.shortcuts import render
from django.http import HttpResponse

from airqo_monitor.get_malfunctions import get_all_channel_malfunctions_cached


def index(request):
    malfunctioning_channels = get_all_channel_malfunctions_cached()

    return render(
    	request,
        "index.html",
        context={"malfunctioning_channels": malfunctioning_channels},
    )


def db(request):
	pass
