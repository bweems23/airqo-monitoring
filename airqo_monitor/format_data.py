from airqo_monitor.external.thingspeak import (
    get_all_channels_by_type,
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
    Gets data from Thingspeak and formats the response into understandable names
    based on the channel type's data format.

    Returns: List of dicts, where each dict is one data entry point
    """
    channel_id = channel.channel_id
    channel_type_name = channel.channel_type.name
    data_format = channel.channel_type.data_format

    data = get_data_for_channel(channel_id, start_time=start_time, end_time=end_time)
    formatted_data = []

    for entry in data:
        entry_data = dict()
        for thingspeak_fieldname, descriptive_name in data_format.items():
            entry_data[descriptive_name] = entry.get(thingspeak_fieldname, None)
        entry_data['type'] = channel_type_name
        entry_data['entry_id'] = entry['entry_id']
        entry_data['channel_id'] = channel_id
        entry_data['created_at'] = entry['created_at']
        formatted_data.append(entry_data)

    return formatted_data


def _update_db_channel_table(channel, channel_type, new_channel_data):
    """
    Given metadata about a Thingspeak channel, update the corresponding
    Channel objects in the database
    """
    channel_name = new_channel_data['name']
    update_fields = []

    # Update that channel with its latest data
    if channel.name != channel_name:
        channel.name = channel_name
        update_fields.append('name')

    if not channel.channel_type or channel.channel_type is not channel_type:
        channel.channel_type = channel_type
        update_fields.append('channel_type')

    # reactivate channel if Thingspeak thinks it's active
    if not channel.is_active and INACTIVE_MONITOR_KEYWORD not in channel_name:
        channel.is_active = True
        update_fields.append('is_active')

    # Deactivate channel if it's no longer active on Thingspeak
    if channel.is_active and INACTIVE_MONITOR_KEYWORD in channel_name:
        channel.is_active = False
        update_fields.append('is_active')

    if update_fields:
        channel.save(update_fields=update_fields)


def update_all_channels_for_channel_type(channel_type):
    """
    Given a channel type, get all channels for this channel type from Thingspeak
    and update them in the DB based on Thingspeak's latest data
    """
    all_channel_data = get_all_channels_by_type(channel_type.name)
    for channel_data in all_channel_data:
        channel, _ = Channel.objects.get_or_create(channel_id=channel_data['id'], channel_type=channel_type)
        _update_db_channel_table(channel, channel_type, channel_data)


def update_all_channel_data():
    """
    Get all channel data from Thingspeak and update in the DB
    """
    channel_types = ChannelType.objects.all()
    for channel_type in channel_types:
        update_all_channels_for_channel_type(channel_type)


def get_and_format_data_for_all_channels(start_time=None, end_time=None):
    """
    Update the channels from Thingspeak, then get and format data between start_time and end_time
    for all active channels.

    Returns: dict {thingspeak_channel_id: {'channel': channel_object, 'data': list of entry point dicts}}
    """
    update_all_channel_data()

    all_channels_dict = dict()

    channels = Channel.objects.filter(is_active=True)
    for channel in channels:
        data = get_and_format_data_for_channel(channel, start_time=start_time, end_time=end_time)
        all_channels_dict[channel.channel_id] = {'channel': channel, 'data': data}

    return all_channels_dict
