from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse

from airqo_monitor.models import Incident

from airqo_monitor.get_malfunctions import (
    get_all_channel_malfunctions
)
from airqo_monitor.models import (
    Channel,
    ChannelNote,
    ChannelType,
    Incident,
)
from airqo_monitor.serializers import (
    ChannelHistorySerializer,
    ChannelSerializer,
    ChannelNoteSerializer,
    ChannelTypeSerializer,
    IncidentSerializer,
)
from airqo_monitor.utils import (
    create_channel_note,
    get_channel_history,
)

def index(request):
    return render(
        request,
        "index.html",
        context={
            "channels": ChannelSerializer(Channel.objects.filter(is_active=True), many=True).data,
            "all_channel_types": ChannelTypeSerializer(ChannelType.objects.all(), many=True).data,
        },
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


def channel_types_list(request):
    channels = Channel.objects.filter(is_active=True)

    return render(
        request,
        "channels_list.html",
        context={
            "channels": ChannelSerializer(channels, many=True).data,
            "all_channel_types": ChannelTypeSerializer(ChannelType.objects.all(), many=True).data,
            "channel_type_name": "",
        }
    )


def channel_type_channels_list(request, channel_type):
    try:
        channel_type = ChannelType.objects.get(name=channel_type)
        channels = Channel.objects.filter(channel_type=channel_type, is_active=True)
    except ChannelType.DoesNotExist:
        raise Http404("Cannot find channel type {}. Possible types are: {}".format(
                channel_type,
                ChannelType.objects.all(),
            )
        )

    return render(
        request,
        "channels_list.html",
        context={
            "channels": ChannelSerializer(channels, many=True).data,
            "all_channel_types": ChannelTypeSerializer(ChannelType.objects.all(), many=True).data,
            "channel_type_name": channel_type,
        }
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


def update_incidents(request):
    get_all_channel_malfunctions()
    return redirect('/')
