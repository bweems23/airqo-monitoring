from airqo_monitor.external.thingspeak import (
    get_all_channels_cached,
    get_data_for_channel,
)
from airqo_monitor.constants import INACTIVE_MONITOR_KEYWORD
from airqo_monitor.models import Channel, ChannelType
from airqo_monitor.objects.data_entry import DataEntry


def parse_field8_metadata(field8):
    """
    Parse string formatted lat,lng,elevation,speed (in mps),num_satellites,hdop into six variables
    """
    return field8.split(',')


def get_and_format_data_for_channel(channel, start_time=None, end_time=None):
    """
    Parses thingspeak json response.
    Field mapping depends on the channel type's data format
    """
    channel_id = channel.channel_id
    channel_type_name = channel.channel_type.name
    data_format = channel.channel_type.data_format

    data = get_data_for_channel(channel_id, start_time=start_time, end_time=end_time)
    formatted_data = []

    for entry in data:
        entry_data = dict()
        for key, value in data_format.items():
            entry_data[value] = entry.get(key, None)
        entry_data['type'] = channel_type_name
        entry_data['entry_id'] = entry['entry_id']
        entry_data['channel_id'] = channel_id
        entry_data['created_at'] = entry['created_at']
        formatted_data.append(entry_data)

    return formatted_data


def update_all_channels_for_channel_type(channel_type):
    """
    Given a channel type, get all channels for this channel type from Thingspeak
    and update them in the DB
    """
    all_channels = get_all_channels_cached()
    channels_for_type = []
    for channel_data in all_channels:
        channel_name = channel_data['name']
        channel_id = channel_data['id']
        channel_tags = channel_data['tags']

        # ignore channels of different type
        tag_found = False
        for tag in channel_tags:
            if tag['name'] == channel_type.name:
                tag_found = True
                break
        if not tag_found:
            continue

        # ignore inactive channels
        if INACTIVE_MONITOR_KEYWORD in channel_name:
            continue

        channel, _ = Channel.objects.get_or_create(channel_id=channel_id)

        update_fields = []
        # Update that channel with its latest data
        if channel.name != channel_name:
            channel.name = channel_name
            update_fields.append('name')

        if not channel.channel_type or channel.channel_type is not channel_type:
            channel.channel_type = channel_type
            update_fields.append('channel_type')

        if not channel.is_active:
            channel.is_active = True
            update_fields.append('is_active')

        if update_fields:
            channel.save(update_fields=update_fields)

        channels_for_type.append(channel)

    return channels_for_type


def update_all_channel_data():
    """
    Get all channel data from Thingspeak and update in the DB
    """
    channel_types = ChannelType.objects.all()
    for channel_type in channel_types:
        update_all_channels_for_channel_type(channel_type)


def get_and_format_data_for_all_channels(start_time=None, end_time=None):
    # Make sure we have the latest data
    update_all_channel_data()

    all_channels_dict = dict()

    channels = Channel.objects.filter(is_active=True)
    for channel in channels:
        data = get_and_format_data_for_channel(channel, start_time=start_time, end_time=end_time)
        all_channels_dict[channel.channel_id] = {'channel': channel, 'data': data}

    return all_channels_dict
