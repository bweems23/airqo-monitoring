from datetime import datetime

from airqo_monitor.constants import LAST_CHANNEL_UPDATE_TIME_GLOBARLVAR_NAME
from airqo_monitor.models import (
    Channel,
    ChannelNote,
    GlobalVariable,
    Incident,
)


def get_int_global_var_value(key):
    var = GlobalVariable.objects.get(key=key)
    return int(var.value)


def get_float_global_var_value(key):
    var = GlobalVariable.objects.get(key=key)
    return float(var.value)


def get_str_global_var_value(key):
    var = GlobalVariable.objects.get(key=key)
    return var.value


def get_channel_history(channel):
    """
    Get an ordered list of all Incidents and Notes for a Channel
    """
    incidents = list(Incident.objects.filter(channel=channel).all())
    notes = list(ChannelNote.objects.filter(channel=channel).all())

    history = incidents + notes
    history.sort(key=lambda x: x.created_at, reverse=True)

    return history


def create_channel_note(channel_id, author, note):
    channel = Channel.objects.get(channel_id=channel_id)

    note = ChannelNote.objects.create(
        author=author,
        note=note,
        channel=channel,
    )

    return note


def update_last_channel_update_time():
    variable = GlobalVariable.objects.get(key=LAST_CHANNEL_UPDATE_TIME_GLOBARLVAR_NAME)
    variable.value = datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M:%SZ')
    variable.save()

