from airqo_monitor.external.thingspeak import (
    get_channel_ids_to_names,
    get_data_for_channel,
)
from airqo_monitor.models import Channel
from airqo_monitor.objects.data_entry import DataEntry


def parse_field8_metadata(field8):
    """
    Parse string formatted lat,lng,elevation,speed (in mps),num_satellites,hdop into six variables
    """
    return field8.split(',')


def get_and_format_data_for_channel(channel_id, start_time=None, end_time=None):
    """
    Parses thingspeak json response.
    Field mapping:
    field1: pm1
    field2: pm2.5
    field3: pm10
    field4: sample period
    field5: latitude
    field6: longtitude
    field7: battery voltage
    field8 (optional): lat,lng,elevation,speed,num_satellites,hdop
    """
    data = get_data_for_channel(channel_id, start_time=start_time, end_time=end_time)
    entry_objects = []
    for entry in data:
        entry_object = DataEntry(
            channel_id=channel_id,
            entry_id=entry['entry_id'],
        )
        entry_object.created_at = entry['created_at']
        entry_object.pm_1 = entry['field1']
        entry_object.pm_2_5 = entry['field2']
        entry_object.pm_10 = entry['field3']
        entry_object.sample_period = entry['field4']
        entry_object.battery_voltage = entry['field7']

        field8 = entry.get('field8', None)
        if field8:
            try:
                lat, lng, altitude, speed, num_satellites, hdop = parse_field8_metadata(field8)
                entry_object.latitude = lat
                entry_object.longitude = lng
                entry_object.altitude = altitude
                entry_object.speed = speed
                entry_object.num_satellites = num_satellites
                entry_object.hdop = hdop
            except ValueError:
                # there must have been a misformatted field, fallback to the old
                # lat and lng fields
                entry_object.latitude = entry['field5']
                entry_object.longitude = entry['field6']
        else:
            entry_object.latitude = entry['field5']
            entry_object.longitude = entry['field6']

        # we currently only have stationary devices active
        entry_object.is_mobile = False

        entry_objects.append(entry_object)
    return entry_objects


def _update_db_channel_table(channel_ids_to_names):
    for channel_id, channel_info in channel_ids_to_names.items():
        channel, _ = Channel.objects.get_or_create(channel_id=channel_id)
        channel_name = channel_info["name"]
        if channel.name != channel_name:
            channel.name = channel_name
            channel.save()


def get_and_format_data_for_all_channels(start_time=None, end_time=None):
    all_channels_dict = get_channel_ids_to_names()

    for channel_id in all_channels_dict.keys():
        data = get_and_format_data_for_channel(channel_id, start_time=start_time, end_time=end_time)
        all_channels_dict[channel_id]["data"] = data

    return all_channels_dict
