from airqo_monitor.constants import LOW_BATTERY_CUTOFF

class MalfunctionDetector(object):
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
