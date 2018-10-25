from airqo_monitor.models import (
    Channel,
    ChannelNote,
    Incident,
)

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