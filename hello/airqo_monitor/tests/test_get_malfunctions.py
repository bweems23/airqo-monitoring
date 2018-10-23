import mock
import unittest

from datetime import datetime, timedelta

from constants import (
    THINGSPEAK_CHANNELS_LIST_URL,
    THINGSPEAK_FEEDS_LIST_URL,
    LOW_BATTERY_CUTOFF,
    SENSOR_PM_2_5_MIN_CUTOFF,
    SENSOR_PM_2_5_MAX_CUTOFF,
)
from models.data_entry import DataEntry
from get_malfunctions import (
    _get_channel_malfunctions,
    _has_low_battery,
    _has_low_reporting_frequency,
    _sensor_is_reporting_outliers,
    get_all_channel_malfunctions,
)

class TestGetMalfunctions(unittest.TestCase):

    sample_channel_data = [
        DataEntry(
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
        DataEntry(
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
        DataEntry(
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

    @mock.patch('get_malfunctions._sensor_is_reporting_outliers')
    @mock.patch('get_malfunctions._has_low_battery')
    @mock.patch('get_malfunctions._has_low_reporting_frequency')
    def test_get_channel_malfunctions(self, _has_low_reporting_frequency_mocker, _has_low_battery_mocker,
                                      _sensor_is_reporting_outliers_mocker):
        _has_low_reporting_frequency_mocker.return_value = True
        _has_low_battery_mocker.return_value = False
        _sensor_is_reporting_outliers_mocker.return_value = False
        malfunctions = _get_channel_malfunctions(self.sample_channel_data)

        assert "low_reporting_frequency" in malfunctions
        assert "low_battery_voltage" not in malfunctions
        assert "reporting_outliers" not in malfunctions
        assert "no_data" not in malfunctions

        # We expect "no_data" to be the returned malfunction when we pass in no data.
        malfunctions = _get_channel_malfunctions([])
        assert "no_data" in malfunctions
        assert "low_reporting_frequency" not in malfunctions


    def test_has_low_battery(self):
        assert _has_low_battery(self.sample_channel_data) == False

        # Set a voltage below the cutoff.
        self.sample_channel_data[-1].battery_voltage = str(LOW_BATTERY_CUTOFF - 0.1)
        assert _has_low_battery(self.sample_channel_data) == True


    def test_has_low_reporting_frequency(self):
        assert _has_low_reporting_frequency(self.sample_channel_data) == True

        # Make the created_at time stamps now so that they look frequent.
        now = datetime.utcnow()
        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.sample_channel_data[0].created_at = now_str
        self.sample_channel_data[1].created_at = now_str
        self.sample_channel_data[2].created_at = now_str
        assert _has_low_reporting_frequency(self.sample_channel_data) == False


    def test_sensor_is_reporting_outliers(self):
        assert _sensor_is_reporting_outliers(self.sample_channel_data) == False


        self.sample_channel_data[0].pm_2_5 = str(SENSOR_PM_2_5_MIN_CUTOFF - 0.1)
        assert _sensor_is_reporting_outliers(self.sample_channel_data) == True

        self.sample_channel_data[0].pm_2_5 = str(SENSOR_PM_2_5_MAX_CUTOFF + 0.1)
        assert _sensor_is_reporting_outliers(self.sample_channel_data) == True


    @mock.patch('get_malfunctions._get_channel_malfunctions')
    @mock.patch('get_malfunctions.get_and_format_data_for_all_channels')
    def test_get_all_channel_malfunctions(self, get_and_format_data_for_all_channels_mocker, _get_channel_malfunctions_mocker):
        get_and_format_data_for_all_channels_mocker.return_value =  {'123': self.sample_channel_data}
        _get_channel_malfunctions_mocker.return_value = ['reporting_outliers']

        assert get_all_channel_malfunctions() == [
            {
                "channel_id": '123',
                "possible_malfunction_reasons": ['reporting_outliers'],
            }
        ]
