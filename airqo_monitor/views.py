from django.shortcuts import render
from django.http import Http404, HttpResponse

from airqo_monitor.get_malfunctions import get_all_channel_malfunctions_cached
from airqo_monitor.models import Channel, Incident
from airqo_monitor.serializers import ChannelSerializer, IncidentSerializer


def index(request):
    malfunctioning_channels = get_all_channel_malfunctions_cached()

    return render(
        request,
        "index.html",
        context={"malfunctioning_channels": malfunctioning_channels},
    )


def db(request):
    pass


def channel_detail(request, channel_id):
    try:
        channel = Channel.objects.get(channel_id=channel_id)
    except Channel.DoesNotExist:
        raise Http404("Cannot find channel. Please make sure the api_key has been stored if it is a private channel.")

    incidents = Incident.objects.filter(channel=channel)
    serialized_incidents = IncidentSerializer(incidents, many=True)

    return render(
        request,
        "channel_detail.html",
        context={
            "channel": ChannelSerializer(channel).data,
            "incidents": serialized_incidents.data,
        },
    )
