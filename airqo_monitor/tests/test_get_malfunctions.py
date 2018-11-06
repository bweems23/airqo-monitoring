import json
import mock

from datetime import datetime, timedelta
from django.test import TestCase

from airqo_monitor.constants import (
    THINGSPEAK_CHANNELS_LIST_URL,
    THINGSPEAK_FEEDS_LIST_URL,
    LAST_CHANNEL_UPDATE_TIME_GLOBARLVAR_NAME,
    LOW_BATTERY_CUTOFF,
    SENSOR_PM_2_5_MIN_CUTOFF,
    SENSOR_PM_2_5_MAX_CUTOFF,
)
from airqo_monitor.objects.data_entry import DataEntry
from airqo_monitor.get_malfunctions import (
    _get_channel_malfunctions,
    get_all_channel_malfunctions,
    update_db,
)
from airqo_monitor.models import (
    Channel,
    ChannelType,
    GlobalVariable,
    Incident,
    MalfunctionReason,
)

class TestGetMalfunctions(TestCase):

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

    def setUp(self):
        self.channel_type, _ = ChannelType.objects.get_or_create(
            name='soil',
            friendly_name='Soil',
            data_format_json=json.dumps({"field1": "pm_1","field2": "pm_2_5","field3": "pm_10","field4": "sample_period","field5": "latitude","field6": "longitude","field7": "battery_voltage","field8": "lat,lng,elevation,speed,num_satellites,hdop"})
        )
        GlobalVariable.objects.create(key=LAST_CHANNEL_UPDATE_TIME_GLOBARLVAR_NAME)

    @mock.patch('airqo_monitor.malfunction_detection.airqo_malfunction_detector.AirqoMalfunctionDetector._sensor_is_reporting_outliers')
    @mock.patch('airqo_monitor.malfunction_detection.base_malfunction_detector.MalfunctionDetector._has_low_battery')
    @mock.patch('airqo_monitor.malfunction_detection.airqo_malfunction_detector.AirqoMalfunctionDetector._has_low_reporting_frequency')
    def test_get_channel_malfunctions(self, _has_low_reporting_frequency_mocker, _has_low_battery_mocker,
                                      _sensor_is_reporting_outliers_mocker):
        _has_low_reporting_frequency_mocker.return_value = True
        _has_low_battery_mocker.return_value = False
        _sensor_is_reporting_outliers_mocker.return_value = False
        malfunctions = _get_channel_malfunctions(self.sample_channel_data, channel_type='airqo')

        assert "low_reporting_frequency" in malfunctions
        assert "low_battery_voltage" not in malfunctions
        assert "reporting_outliers" not in malfunctions
        assert "no_data" not in malfunctions

        # We expect "no_data" to be the returned malfunction when we pass in no data.
        malfunctions = _get_channel_malfunctions([], channel_type='airqo')
        assert "no_data" in malfunctions
        assert "low_reporting_frequency" not in malfunctions

    @mock.patch('airqo_monitor.get_malfunctions.update_db')
    @mock.patch('airqo_monitor.get_malfunctions._get_channel_malfunctions')
    @mock.patch('airqo_monitor.get_malfunctions.get_and_format_data_for_all_channels')
    def test_get_all_channel_malfunctions(self, get_and_format_data_for_all_channels_mocker, _get_channel_malfunctions_mocker, update_db_mocker):
        update_db_mocker.return_value = None
        channel1 = Channel.objects.create(channel_id=5555, name='channel5555', channel_type=self.channel_type)
        get_and_format_data_for_all_channels_mocker.return_value =  {
            5555: {'channel': channel1, 'data': self.sample_channel_data}
        }
        _get_channel_malfunctions_mocker.return_value = ['reporting_outliers']
        all_channel_malfunctions = get_all_channel_malfunctions()
        assert all_channel_malfunctions == [
            {
                'name': 'channel5555',
                'channel_id': 5555,
                'possible_malfunction_reasons': ['reporting_outliers'],
            }
        ]

    def test_update_db_creates_incidents(self):
        reason = MalfunctionReason.objects.create(name='reason', description='Reason')
        channel = Channel.objects.create(channel_id='111', name='Test Channel', channel_type=self.channel_type)

        channels = [
            {
            'channel_id': '111',
            'possible_malfunction_reasons': ['reason']
            }
        ]
        update_db(channels)

        incident = Incident.objects.last()
        assert incident.channel == channel
        assert incident.malfunction_reason == reason
        assert incident.resolved_at is None

    def test_update_db_resolves_incidents(self):
        reason = MalfunctionReason.objects.create(name='reason', description='Reason')
        channel = Channel.objects.create(channel_id='1234', name='Test Channel', channel_type=self.channel_type)
        incident = Incident.objects.create(channel=channel, malfunction_reason=reason)

        channels = [
            {
            'channel_id': '1234',
            'possible_malfunction_reasons': []
            }
        ]
        update_db(channels)

        incident = Incident.objects.get(id=incident.id)
        assert incident.resolved_at is not None
