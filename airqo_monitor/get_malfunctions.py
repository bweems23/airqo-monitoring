from datetime import datetime, timedelta
from werkzeug.contrib.cache import SimpleCache
from copy import deepcopy

from airqo_monitor.models import Incident, Channel, MalfunctionReason

from airqo_monitor.format_data import get_and_format_data_for_all_channels
from airqo_monitor.constants import (
    AIRQO_CHANNEL_TYPE,
    LOW_BATTERY_CUTOFF,
    NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION,
    SENSOR_PM_2_5_MIN_CUTOFF,
    SENSOR_PM_2_5_MAX_CUTOFF,
    SOIL_CHANNEL_TYPE,
    ALLOWABLE_OUTLIER_SENSOR_RATIO,
    NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION,
    MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS,
)

cache = SimpleCache()


def _get_channel_malfunctions(channel_data, channel_type):
    """Use channel_data to get a list of malfunctions that may be occuring with a channel.

    Returns: a list of potential malfunctions. Potential malfunctions include:
        - "low_battery_voltage": Channel data indicates that the device is running low on battery
        - "low_reporting_frequency": The device is not reporting data fast enough or at all.
        - "reporting_outliers": The sensor is reporting readings that are outside a reasonable range.
        - "no_data": The channel_data list was empty.
    """
    malfunction_list = []
    if len(channel_data) == 0:
        malfunction_list.append("no_data")
    else:
        if _has_low_battery(channel_data, channel_type):
            malfunction_list.append("low_battery_voltage")
        if _has_low_reporting_frequency(channel_data, channel_type):
            malfunction_list.append("low_reporting_frequency")
        if _sensor_is_reporting_outliers(channel_data, channel_type):
            malfunction_list.append("reporting_outliers")

    return malfunction_list


def _has_low_battery(channel_data, channel_type):
    """Determine whether the channel has low battery. channel_data can't be empty."""
    assert len(channel_data) > 0
    if channel_type == AIRQO_CHANNEL_TYPE:
        last_voltage = float(channel_data[-1].get('battery_voltage'))
        return last_voltage < LOW_BATTERY_CUTOFF


def _has_low_reporting_frequency(channel_data, channel_type):
    """Determine whether the channel is reporting data at a lower frequency than expected."""
    assert len(channel_data) > 0

    if channel_type == AIRQO_CHANNEL_TYPE:
        index_to_verify = min(len(channel_data), NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION)
        report_to_verify = channel_data[-1 * index_to_verify]
        report_timestamp = datetime.strptime(report_to_verify.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')

        # The cutoff time is now minus MINIMUM_REPORT_FREQUENCY_SECONDS seconds per report being evaluated.
        # The number of reports being evaluated is determined by the index_to_verify.
        cutoff_time = datetime.utcnow() - timedelta(seconds=MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS * index_to_verify)

        # If the report timestamp is earlier than the cutoff time, that means that there is too much time passing
        # between each point being reported.
        return report_timestamp < cutoff_time


def _sensor_is_reporting_outliers(channel_data, channel_type):
    """Determine whether the sensor is reporting points outside the reasonable range.

    Presence of outlier points may indicated an obstructed sensor.
    """
    assert len(channel_data) > 0
    if channel_type == AIRQO_CHANNEL_TYPE:
        num_points = min(NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION, len(channel_data))
        is_outlier = lambda pm_2_5: pm_2_5 < SENSOR_PM_2_5_MIN_CUTOFF or pm_2_5 > SENSOR_PM_2_5_MAX_CUTOFF
        extreme_reads = [entry for entry in channel_data[-1 * num_points:] if is_outlier(float(entry.get('pm_2_5')))]
        return len(extreme_reads) > num_points * ALLOWABLE_OUTLIER_SENSOR_RATIO


def update_db(channels):
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
    cached_value = cache.get('channel-malfunctions')
    if cached_value is None:
        cached_value = get_all_channel_malfunctions()
        cache.set('channel-malfunctions', cached_value, timeout=5 * 60)
    return cached_value
