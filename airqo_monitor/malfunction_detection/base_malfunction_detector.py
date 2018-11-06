from airqo_monitor.constants import LOW_BATTERY_CUTOFF

class MalfunctionDetector(object):

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

    def _has_low_battery(self, channel_data):
        """Determine whether the channel has low battery. channel_data can't be empty."""
        assert len(channel_data) > 0
        last_voltage = float(channel_data[-1].get('battery_voltage'))
        return last_voltage < LOW_BATTERY_CUTOFF

    def _has_no_data(self, channel_data):
        return len(channel_data) == 0

    def _sensor_is_reporting_outliers(self, channel_data):
        return False

    def _has_low_reporting_frequency(self, channel_data):
        return False
