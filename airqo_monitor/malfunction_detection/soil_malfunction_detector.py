from airqo_monitor.malfunction_detection.base_malfunction_detector import MalfunctionDetector


class SoilMalfunctionDetector(MalfunctionDetector):
    def _sensor_is_reporting_outliers(self, channel_data):
        """Determine whether the sensor is reporting points outside the reasonable range.

        Presence of outlier points may indicated an obstructed sensor.
        """
        return False

    def _has_low_reporting_frequency(self, channel_data):
        """Determine whether the channel is reporting data at a lower frequency than expected."""
        return False
