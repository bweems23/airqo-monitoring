from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse

from airqo_monitor.models import Incident

from airqo_monitor.get_malfunctions import get_all_channel_malfunctions_cached
from airqo_monitor.models import (
    Channel,
    ChannelNote,
    Incident,
)
from airqo_monitor.serializers import (
    ChannelHistorySerializer,
    ChannelSerializer,
    ChannelNoteSerializer,
    IncidentSerializer,
)
from airqo_monitor.utils import (
    create_channel_note,
    get_channel_history,
)

def index(request):
    # TODO make this get called in a cron job
    # for now we're just calling it every time the homepage is reloaded
    get_all_channel_malfunctions_cached()

    return render(
        request,
        "index.html",
        context={"channels": ChannelSerializer(Channel.objects.all(), many=True).data},
    )


def incidents(request):
	incidents = Incident.objects.all()
	return render(request, "incidents.html", context={"incidents": incidents})


def db(request):
    pass


def channel_detail(request, channel_id):
    try:
        channel = Channel.objects.get(channel_id=channel_id)
    except Channel.DoesNotExist:
        raise Http404("Cannot find channel. Please make sure the api_key has been stored if it is a private channel.")

    history = get_channel_history(channel)

    return render(
        request,
        "channel_detail.html",
        context={
            "channel": ChannelSerializer(channel).data,
            "history": ChannelHistorySerializer(history, many=True).data,
        },
    )

def channel_notes(request):
    if request.method == 'POST':
        note = request.POST.get('note')
        author = request.POST.get('author')
        channel_id = request.POST.get('channel')
        
        create_channel_note(
            author=author,
            note=note,
            channel_id=channel_id,
        )

    redirect_url = '/channels/{}/'.format(channel_id)
    return redirect(redirect_url)
