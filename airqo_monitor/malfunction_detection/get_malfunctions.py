from datetime import datetime, timedelta
from werkzeug.contrib.cache import SimpleCache
from copy import deepcopy

from airqo_monitor.models import Incident, Channel, MalfunctionReason

from airqo_monitor.format_data import get_and_format_data_for_all_channels
from airqo_monitor.constants import (
    AIRQO_CHANNEL_TYPE,
    SOIL_CHANNEL_TYPE,
)
from airqo_monitor.malfunction_detection import (
    AirqoMalfunctionDetector,
    SoilMalfunctionDetector,
    MalfunctionDetector,
)
from airqo_monitor.utils import update_last_channel_update_time

cache = SimpleCache()


def _get_channel_malfunctions(channel_data, channel_type):
    """
    Use channel_data to get a list of malfunctions that may be occuring with a channel.

    Returns: a list of potential malfunctions. Potential malfunctions include:
        - "low_battery_voltage": Channel data indicates that the device is running low on battery
        - "low_reporting_frequency": The device is not reporting data fast enough or at all.
        - "reporting_outliers": The sensor is reporting readings that are outside a reasonable range.
        - "no_data": The channel_data list was empty.
    """
    malfunction_detector = MalfunctionDetector()
    if channel_type == AIRQO_CHANNEL_TYPE:
        malfunction_detector = AirqoMalfunctionDetector()
    elif channel_type == SOIL_CHANNEL_TYPE:
        malfunction_detector = SoilMalfunctionDetector()

    return malfunction_detector.get_malfunctions(channel_data)


def update_db(channels):
    """
    Given a list of channels and their active malfunctions, create or resolve Incidents
    to reflect the current status.
    """
    for channel in channels:
        channel_object = Channel.objects.filter(channel_id=channel["channel_id"]).first()

        # Check for existing incidents and resolve ones that have gone away.
        existing_channel_incidents = Incident.objects.filter(channel=channel_object, resolved_at__isnull=True)
        current_incident_reasons = deepcopy(channel["possible_malfunction_reasons"])
        for incident in existing_channel_incidents:
            reason_name = incident.malfunction_reason.name
            if reason_name not in current_incident_reasons:
                # If the incident is no longer reported, we consider it resolved.
                incident.resolved_at = datetime.now()
                incident.save()
            else:
                # If the incident already exists we don't want to create a new Incident object.
                current_incident_reasons.remove(reason_name)

        # Create new incidents and their reason links.
        if current_incident_reasons:
            # Create one incident per reason.
            for malfunction_reason_name in current_incident_reasons:
                # Create the incident and connect it to a reason.
                malfunction_reason = MalfunctionReason.objects.filter(name=malfunction_reason_name).first()
                incident = Incident.objects.create(channel=channel_object, malfunction_reason=malfunction_reason)

    update_last_channel_update_time()


def get_all_channel_malfunctions():
    """Generate a list of malfunctions for all channels.

    Returns: A dict keyed by the channel id. The value is a list of potential concerns about a sensor.
    """
    channels = []
    start_time = datetime.utcnow() - timedelta(days=1)
    all_channels_info = get_and_format_data_for_all_channels(start_time=start_time)
    for channel_id, channel_info in all_channels_info.items():
        channel = channel_info['channel']
        possible_malfunctions = _get_channel_malfunctions(channel_info['data'], channel.channel_type.name)
        channels.append(
            {
                "name": channel.name,
                "channel_id": channel_id,
                "possible_malfunction_reasons": possible_malfunctions,
            }
        )

    update_db(channels)
    return channels


def get_all_channel_malfunctions_cached():
    """
    Cached wrapper around get_all_channel_malfunctions
    """
    cached_value = cache.get('channel-malfunctions')
    if cached_value is None:
        cached_value = get_all_channel_malfunctions()
        cache.set('channel-malfunctions', cached_value, timeout=5 * 60)
    return cached_value
