from datetime import datetime, timedelta

from airqo_monitor.constants import (
    LOW_BATTERY_MALFUNCTION_REASON_STR,
    LOW_REPORTING_FREQUENCY_MALFUNCTION_REASON_STR,
    NO_DATA_MALFUNCTION_REASON_STR,
    REPORTING_OUTLIERS_MALFUNCTION_REASON_STR,
)

from airqo_monitor.malfunction_detection.base_malfunction_detector import MalfunctionDetector
from airqo_monitor.utils import get_float_global_var_value, get_int_global_var_value


class SoilMalfunctionDetector(MalfunctionDetector):

    def get_malfunctions(self, channel_data):
        malfunction_list = []

        if self._has_no_data(channel_data):
            malfunction_list.append(NO_DATA_MALFUNCTION_REASON_STR)
        else:
            if self._has_low_battery(channel_data):
                malfunction_list.append(LOW_BATTERY_MALFUNCTION_REASON_STR)
            if self._has_low_reporting_frequency(channel_data):
                malfunction_list.append(LOW_REPORTING_FREQUENCY_MALFUNCTION_REASON_STR)
            if self._sensor_is_reporting_outliers(channel_data):
                malfunction_list.append(REPORTING_OUTLIERS_MALFUNCTION_REASON_STR)

        return malfunction_list

    def _sensor_is_reporting_outliers(self, channel_data):
        """Determine whether the sensor is reporting points outside the reasonable range.

        Presence of outlier points may indicated an obstructed sensor.
        """
        assert len(channel_data) > 0
        num_points = min(get_int_global_var_value('SOIL_NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION'), len(channel_data))
        is_outlier = lambda pm_2_5: pm_2_5 < get_float_global_var_value('SOIL_SENSOR_PM_2_5_MIN_CUTOFF') or pm_2_5 > get_float_global_var_value('SOIL_SENSOR_PM_2_5_MAX_CUTOFF')
        extreme_reads = [entry for entry in channel_data[-1 * num_points:] if is_outlier(float(entry.get('pm_2_5')))]
        return len(extreme_reads) > num_points * get_float_global_var_value('SOIL_ALLOWABLE_OUTLIER_SENSOR_RATIO')

    def _has_low_reporting_frequency(self, channel_data):
        """Determine whether the channel is reporting data at a lower frequency than expected."""
        assert len(channel_data) > 0

        index_to_verify = min(len(channel_data), get_int_global_var_value('SOIL_NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION'))
        report_to_verify = channel_data[-1 * index_to_verify]
        report_timestamp = datetime.strptime(report_to_verify.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')

        # The cutoff time is now minus MINIMUM_REPORT_FREQUENCY_SECONDS seconds per report being evaluated.
        # The number of reports being evaluated is determined by the index_to_verify.
        cutoff_time = datetime.utcnow() - timedelta(seconds=get_int_global_var_value('SOIL_MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS') * index_to_verify)

        # If the report timestamp is earlier than the cutoff time, that means that there is too much time passing
        # between each point being reported.
        return report_timestamp < cutoff_time
