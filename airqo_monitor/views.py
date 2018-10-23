from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting


from airqo_monitor.external.thingspeak import get_all_channel_ids
from airqo_monitor.get_malfunctions import get_all_channel_malfunctions_cached

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    malfunctioning_channels = get_all_channel_malfunctions_cached()

    return render(
    	request,
        "index.html",
        context={"malfunctioning_channels": malfunctioning_channels},
    )


def db(request):
	pass
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greeting.objects.all()

    # return render(request, "db.html", {"greetings": greetings})
