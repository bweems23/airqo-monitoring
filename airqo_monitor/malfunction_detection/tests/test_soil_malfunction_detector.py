import mock

from django.test import TestCase

from airqo_monitor.malfunction_detection import SoilMalfunctionDetector
from airqo_monitor.tests.utils import create_malfunction_global_vars
from airqo_monitor.utils import get_float_global_var_value


class TestSoilMalfunctionDetector(TestCase):
    sample_channel_data = [
        dict(
            battery_voltage=u'4.50',
            channel_id=324682,
            created_at=u'2018-10-22T09:00:52Z',
            entry_id=82678,
            latitude=u'1000.000000',
            longitude=u'1000.000000',
            pm_1=u'0.89',
            pm_10=u'3.97',
            pm_2_5=u'1.80',
            sample_period=u'1.39'
        ),
        dict(
            battery_voltage=u'4.50',
            channel_id=324682,
            created_at=u'2018-10-22T09:00:52Z',
            entry_id=82678,
            latitude=u'1000.000000',
            longitude=u'1000.000000',
            pm_1=u'0.89',
            pm_10=u'3.97',
            pm_2_5=u'1.80',
            sample_period=u'1.39'
        ),
        dict(
            battery_voltage=u'4.50',
            channel_id=324682,
            created_at=u'2018-10-22T09:00:52Z',
            entry_id=82678,
            latitude=u'1000.000000',
            longitude=u'1000.000000',
            pm_1=u'0.89',
            pm_10=u'3.97',
            pm_2_5=u'1.80',
            sample_period=u'1.39'
        ),
    ]

    def setup(self):
        pass

    @mock.patch('airqo_monitor.malfunction_detection.base_malfunction_detector.MalfunctionDetector._has_no_data')
    @mock.patch('airqo_monitor.malfunction_detection.base_malfunction_detector.MalfunctionDetector._has_low_battery')
    def test_get_malfunctions_no_malfunctions(self, low_battery_mocker, no_data_mocker):
        low_battery_mocker.return_value = False
        no_data_mocker.return_value = False

        detector = SoilMalfunctionDetector()
        assert detector.get_malfunctions(channel_data=[]) == []

    @mock.patch('airqo_monitor.malfunction_detection.base_malfunction_detector.MalfunctionDetector._has_low_battery')
    @mock.patch('airqo_monitor.malfunction_detection.soil_malfunction_detector.SoilMalfunctionDetector._sensor_is_reporting_outliers')
    @mock.patch('airqo_monitor.malfunction_detection.soil_malfunction_detector.SoilMalfunctionDetector._has_low_reporting_frequency')
    def test_get_malfunctions_all_malfunctioning(self, low_frequency_mocker, outliers_mocker, low_battery_mocker):
        low_battery_mocker.return_value = True
        low_frequency_mocker.return_value = True
        outliers_mocker.return_value = True

        detector = SoilMalfunctionDetector()
        assert detector.get_malfunctions(channel_data=['data']) == ['low_battery_voltage', 'low_reporting_frequency', 'reporting_outliers']

    @mock.patch('airqo_monitor.malfunction_detection.base_malfunction_detector.MalfunctionDetector._has_no_data')
    def test_get_malfunctions_all_malfunctioning_no_data(self, no_data_mocker):
        no_data_mocker.return_value = True

        detector = SoilMalfunctionDetector()
        assert detector.get_malfunctions(channel_data=[]) == ['no_data']

    def test_has_no_data(self):
        detector = SoilMalfunctionDetector()
        assert detector._has_no_data([])
        assert not detector._has_no_data(['imdata'])

    def test_has_low_battery(self):
        create_malfunction_global_vars()
        detector = SoilMalfunctionDetector()

        assert detector._has_low_battery(self.sample_channel_data) == False

        # Set a voltage below the cutoff.
        self.sample_channel_data[-1]['battery_voltage'] = str(get_float_global_var_value('LOW_BATTERY_CUTOFF') - 0.1)
        assert detector._has_low_battery(self.sample_channel_data) == True

    def test_sensor_is_reporting_outliers(self):
        detector = SoilMalfunctionDetector()
        assert not detector._sensor_is_reporting_outliers([])

    def test_has_low_reporting_frequency(self):
        detector = SoilMalfunctionDetector()
        assert not detector._has_low_reporting_frequency([])