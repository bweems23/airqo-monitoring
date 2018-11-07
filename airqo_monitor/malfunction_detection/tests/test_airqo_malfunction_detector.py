import mock

from datetime import datetime
from django.test import TestCase

from airqo_monitor.constants import (
    LOW_BATTERY_CUTOFF,
)
from airqo_monitor.malfunction_detection import AirqoMalfunctionDetector
from airqo_monitor.utils import get_float_global_var_value
from airqo_monitor.tests.utils import create_malfunction_global_vars


class TestAirqoMalfunctionDetector(TestCase):
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
    @mock.patch('airqo_monitor.malfunction_detection.airqo_malfunction_detector.AirqoMalfunctionDetector._sensor_is_reporting_outliers')
    @mock.patch('airqo_monitor.malfunction_detection.airqo_malfunction_detector.AirqoMalfunctionDetector._has_low_reporting_frequency')
    def test_get_malfunctions_no_malfunctions(self, low_frequency_mocker, outliers_mocker, low_battery_mocker, no_data_mocker):
        low_battery_mocker.return_value = False
        no_data_mocker.return_value = False
        low_frequency_mocker.return_value = False
        outliers_mocker.return_value = False

        detector = AirqoMalfunctionDetector()
        assert detector.get_malfunctions(channel_data=[]) == []

    @mock.patch('airqo_monitor.malfunction_detection.base_malfunction_detector.MalfunctionDetector._has_low_battery')
    @mock.patch('airqo_monitor.malfunction_detection.airqo_malfunction_detector.AirqoMalfunctionDetector._sensor_is_reporting_outliers')
    @mock.patch('airqo_monitor.malfunction_detection.airqo_malfunction_detector.AirqoMalfunctionDetector._has_low_reporting_frequency')
    def test_get_malfunctions_all_malfunctioning(self, low_frequency_mocker, outliers_mocker, low_battery_mocker):
        low_battery_mocker.return_value = True
        low_frequency_mocker.return_value = True
        outliers_mocker.return_value = True

        detector = AirqoMalfunctionDetector()
        assert detector.get_malfunctions(channel_data=['data']) == ['low_battery_voltage', 'low_reporting_frequency', 'reporting_outliers']

    @mock.patch('airqo_monitor.malfunction_detection.base_malfunction_detector.MalfunctionDetector._has_no_data')
    def test_get_malfunctions_all_malfunctioning_no_data(self, no_data_mocker):
        no_data_mocker.return_value = True

        detector = AirqoMalfunctionDetector()
        assert detector.get_malfunctions(channel_data=[]) == ['no_data']

    def test_has_no_data(self):
        detector = AirqoMalfunctionDetector()
        assert detector._has_no_data([])
        assert not detector._has_no_data(['imdata'])

    def test_has_low_battery(self):
        detector = AirqoMalfunctionDetector()

        assert detector._has_low_battery(self.sample_channel_data) == False

        # Set a voltage below the cutoff.
        self.sample_channel_data[-1]['battery_voltage'] = str(LOW_BATTERY_CUTOFF - 0.1)
        assert detector._has_low_battery(self.sample_channel_data) == True

    def test_has_low_reporting_frequency(self):
        create_malfunction_global_vars()
        detector = AirqoMalfunctionDetector()

        assert detector._has_low_reporting_frequency(self.sample_channel_data) == True

        # Make the created_at time stamps now so that they look frequent.
        now = datetime.utcnow()
        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.sample_channel_data[0]['created_at'] = now_str
        self.sample_channel_data[1]['created_at'] = now_str
        self.sample_channel_data[2]['created_at'] = now_str
        assert detector._has_low_reporting_frequency(self.sample_channel_data) == False


    def test_sensor_is_reporting_outliers(self):
        create_malfunction_global_vars()
        detector = AirqoMalfunctionDetector()

        assert detector._sensor_is_reporting_outliers(self.sample_channel_data) == False


        self.sample_channel_data[0]['pm_2_5'] = str(get_float_global_var_value('SENSOR_PM_2_5_MIN_CUTOFF') - 0.1)
        assert detector._sensor_is_reporting_outliers(self.sample_channel_data) == True

        self.sample_channel_data[0]['pm_2_5'] = str(get_float_global_var_value('SENSOR_PM_2_5_MAX_CUTOFF') + 0.1)
        assert detector._sensor_is_reporting_outliers(self.sample_channel_data) == True
