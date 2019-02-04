import pytz

from datetime import datetime
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.utils.safestring import mark_safe
import json as simplejson
from datetime import datetime, timedelta

from airqo_monitor.constants import (
    PYTZ_KAMPALA_STRING,
    LAST_CHANNEL_UPDATE_TIME_GLOBARLVAR_NAME,
)
from airqo_monitor.models import Incident
from airqo_monitor.malfunction_detection.get_malfunctions import (
    get_all_channel_malfunctions
)
from airqo_monitor.format_data import (
    get_and_format_heatmap_data_for_all_channels,
    get_and_format_heatmap_data_for_channels,
)
from airqo_monitor.models import (
    Channel,
    ChannelNote,
    ChannelType,
    GlobalVariable,
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
    local_tz = pytz.timezone(PYTZ_KAMPALA_STRING)
    last_update = GlobalVariable.objects.get(key=LAST_CHANNEL_UPDATE_TIME_GLOBARLVAR_NAME)
    last_update_datetime = datetime.strptime(last_update.value,'%Y-%m-%dT%H:%M:%SZ').astimezone(local_tz)
    return render(
        request,
        "index.html",
        context={
            "channels": ChannelSerializer(Channel.objects.filter(is_active=True), many=True).data,
            "all_channel_types": ChannelTypeSerializer(ChannelType.objects.all(), many=True).data,
            "last_update_time": datetime.strftime(last_update_datetime,'%d/%m/%Y at %H:%M')
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

def heatmap(request):
    start_time = datetime.utcnow() - timedelta(days=1)
    heatmap_data = get_and_format_heatmap_data_for_all_channels(start_time=start_time)
    heatmap_json = simplejson.dumps(heatmap_data)
    return render(request, "heatmap.html", context={"geojson_points": mark_safe(heatmap_data)})

def heatmap_with_filter(request, channel_ids):
    """
    Takes in comma separated list of thingspeak channel_ids and filters heatmap data to
    only show data for those channels.
    """
    start_time = datetime.utcnow() - timedelta(days=1)
    heatmap_data = get_and_format_heatmap_data_for_channels(start_time=start_time, channel_ids=channel_ids.split(','))
    heatmap_json = simplejson.dumps(heatmap_data)
    return render(request, "heatmap.html", context={"geojson_points": mark_safe(heatmap_data)})
