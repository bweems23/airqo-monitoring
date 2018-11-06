from airqo_monitor.malfunction_detection.base_malfunction_detector import MalfunctionDetector


class SoilMalfunctionDetector(MalfunctionDetector):

    def get_malfunctions(self, channel_data):
        malfunction_list = []

        if self._has_no_data(channel_data):
            malfunction_list.append("no_data")
        else:
            if self._has_low_battery(channel_data):
                malfunction_list.append("low_battery_voltage")
            if self._has_low_reporting_frequency(channel_data):
                malfunction_list.append("low_reporting_frequency")
            if self._sensor_is_reporting_outliers(channel_data):
                malfunction_list.append("reporting_outliers")

        return malfunction_list

    def _sensor_is_reporting_outliers(self, channel_data):
        """Determine whether the sensor is reporting points outside the reasonable range.

        Presence of outlier points may indicated an obstructed sensor.
        """
        return False

    def _has_low_reporting_frequency(self, channel_data):
        """Determine whether the channel is reporting data at a lower frequency than expected."""
        return False
