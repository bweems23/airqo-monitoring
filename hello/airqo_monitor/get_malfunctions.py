from datetime import datetime, timedelta

from format_data import get_and_format_data_for_all_channels
from constants import (
    LOW_BATTERY_CUTOFF,
    NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION,
    SENSOR_PM_2_5_MIN_CUTOFF,
    SENSOR_PM_2_5_MAX_CUTOFF,
    ALLOWABLE_OUTLIER_SENSOR_RATIO,
    NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION,
    MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS,
)


def _get_channel_malfunctions(channel_data):
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
        if _has_low_battery(channel_data):
            malfunction_list.append("low_battery_voltage")
        if _has_low_reporting_frequency(channel_data):
            malfunction_list.append("low_reporting_frequency")
        if _sensor_is_reporting_outliers(channel_data):
            malfunction_list.append("reporting_outliers")

    return malfunction_list


def _has_low_battery(channel_data):
    """Determine whether the channel has low battery. channel_data can't be empty."""
    assert len(channel_data) > 0
    last_voltage = float(channel_data[-1].battery_voltage)
    return last_voltage < LOW_BATTERY_CUTOFF


def _has_low_reporting_frequency(channel_data):
    """Determine whether the channel is reporting data at a lower frequency than expected."""
    assert len(channel_data) > 0
    index_to_verify = min(len(channel_data), NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION)
    report_to_verify = channel_data[-1 * index_to_verify]
    report_timestamp = datetime.strptime(report_to_verify.created_at, '%Y-%m-%dT%H:%M:%SZ')

    # The cutoff time is now minus MINIMUM_REPORT_FREQUENCY_SECONDS seconds per report being evaluated.
    # The number of reports being evaluated is determined by the index_to_verify.
    cutoff_time = datetime.utcnow() - timedelta(seconds=MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS * index_to_verify)

    # If the report timestamp is earlier than the cutoff time, that means that there is too much time passing
    # between each point being reported.
    return report_timestamp < cutoff_time


def _sensor_is_reporting_outliers(channel_data):
    """Determine whether the sensor is reporting points outside the reasonable range.

    Presence of outlier points may indicated an obstructed sensor.
    """
    assert len(channel_data) > 0
    num_points = min(NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION, len(channel_data))
    is_outlier = lambda pm_2_5: pm_2_5 < SENSOR_PM_2_5_MIN_CUTOFF or pm_2_5 > SENSOR_PM_2_5_MAX_CUTOFF
    extreme_reads = [entry for entry in channel_data[-1 * num_points:] if is_outlier(float(entry.pm_2_5))]
    return len(extreme_reads) > num_points * ALLOWABLE_OUTLIER_SENSOR_RATIO

def get_all_channel_malfunctions():
    """Generate a list of malfunctions for all channels.

    Returns: A dict keyed by the channel id. The value is a list of potential concerns about a sensor.
    """
    malfunctions = []
    start_time = datetime.utcnow() - timedelta(days=1)
    data = get_and_format_data_for_all_channels(start_time=start_time)
    for channel_id, channel_data in data.items():
        malfunctions.append(
            {
                "channel_id": channel_id,
                "possible_malfunction_reasons": _get_channel_malfunctions(channel_data),
            }
        )


    return malfunctions
