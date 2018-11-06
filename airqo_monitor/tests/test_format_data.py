import json
import mock

from bunch import Bunch
from datetime import datetime, timedelta
from django.test import TestCase

from airqo_monitor.models import Channel, ChannelType
from airqo_monitor.constants import (
    THINGSPEAK_CHANNELS_LIST_URL,
    THINGSPEAK_FEEDS_LIST_URL,
)
from airqo_monitor.objects.data_entry import DataEntry
from airqo_monitor.external.thingspeak import (
    get_data_for_channel,
)
from airqo_monitor.format_data import (
    get_and_format_data_for_all_channels,
    get_and_format_data_for_channel,
)


class TestFormatData(TestCase):

    sample_json_entries = [
        {
            u'field2': u'36.00',
            u'field3': u' 6.30',
            u'created_at': u'2017-03-26T22:53:55Z',
            u'field1': u'35.00',
            u'field6': u'1',
            u'field7': u'16',
            u'field4': u' 3400.07',
            u'field5': u'172',
            u'entry_id': 1
        },
        {
            u'field2': u'37.00',
            u'field3': u' 6.40',
            u'created_at': u'2017-03-27T22:53:55Z',
            u'field1': u'36.00',
            u'field6': u'2',
            u'field7': u'17',
            u'field4': u' 3400.08',
            u'field5': u'173',
            u'entry_id': 2
        },
        {
            u'field2': u'38.00',
            u'field3': u' 6.50',
            u'created_at': u'2017-03-28T22:53:55Z',
            u'field1': u'37.00',
            u'field6': u'3',
            u'field7': u'18',
            u'field4': u' 3400.09',
            u'field5': u'174',
            u'entry_id': 3
        },
    ]

    sample_data_format = {
        'field1': 'pm_1',
        'field2': 'pm_2_5',
        'field3': 'pm_10',
        'field4': 'sample_period',
        'field5': 'latitude',
        'field6': 'longitude',
        'field7': 'battery_voltage',
        'field8': 'lat,lng,elevation,speed,num_satellites,hdop'
    }

    def setUp(self):
        self.channel_type, _ = ChannelType.objects.get_or_create(name='airqo', data_format_json=json.dumps(self.sample_data_format))

    @mock.patch('airqo_monitor.format_data.get_data_for_channel')
    def test_get_and_format_data_for_channel(self, get_data_for_channel_mocker):
        get_data_for_channel_mocker.return_value = self.sample_json_entries

        data = get_and_format_data_for_channel(Bunch(channel_id=123, channel_type=Bunch(name='airqo', data_format=self.sample_data_format)))
        assert data[0].get('created_at') == '2017-03-26T22:53:55Z'
        assert data[0].get('channel_id') == 123
        assert data[0].get('entry_id') == 1
        assert data[0].get('pm_1') == '35.00'
        assert data[0].get('pm_2_5') == '36.00'
        assert data[0].get('pm_10') == ' 6.30'
        assert data[0].get('sample_period') == ' 3400.07'
        assert data[0].get('latitude') == '172'
        assert data[0].get('longitude') == '1'
        assert data[0].get('battery_voltage') == '16'

        assert data[1].get('channel_id') == 123
        assert data[1].get('entry_id') == 2

        assert data[2].get('channel_id') == 123
        assert data[2].get('entry_id') == 3

    @mock.patch('airqo_monitor.format_data.get_data_for_channel')
    def test_get_and_format_data_for_channel_with_field8(self, get_data_for_channel_mocker):
        sample_json_entries = self.sample_json_entries
        sample_json_entries[0]['field8'] = '6,7,8,9,10,11'

        get_data_for_channel_mocker.return_value = sample_json_entries

        data = get_and_format_data_for_channel(Bunch(channel_id=123, channel_type=Bunch(name='airqo', data_format=self.sample_data_format)))
        assert data[0].get('created_at') == '2017-03-26T22:53:55Z'
        assert data[0].get('channel_id') == 123
        assert data[0].get('entry_id') == 1
        assert data[0].get('pm_1') == '35.00'
        assert data[0].get('pm_2_5') == '36.00'
        assert data[0].get('pm_10') == ' 6.30'
        assert data[0].get('sample_period') == ' 3400.07'
        assert data[0].get('latitude') == '172'
        assert data[0].get('longitude') == '1'
        assert data[0].get('battery_voltage') == '16'
        assert data[0].get('lat,lng,elevation,speed,num_satellites,hdop') == '6,7,8,9,10,11'

        assert data[1].get('channel_id') == 123
        assert data[1].get('entry_id') == 2
        assert data[1].get('lat,lng,elevation,speed,num_satellites,hdop') is None

        assert data[2].get('channel_id') == 123
        assert data[2].get('entry_id') == 3
        assert data[2].get('lat,lng,elevation,speed,num_satellites,hdop') is None

    @mock.patch('airqo_monitor.format_data.get_data_for_channel')
    def test_get_and_format_data_for_channel_with_misformatted_field8_doesnt_crash(self, get_data_for_channel_mocker):
        sample_json_entries = self.sample_json_entries
        sample_json_entries[0]['field8'] = '6,7,8,9,10'

        get_data_for_channel_mocker.return_value = sample_json_entries

        data = get_and_format_data_for_channel(Bunch(channel_id=123, channel_type=Bunch(name='airqo', data_format=self.sample_data_format)))

        assert data[0].get('latitude') == '172'
        assert data[0].get('longitude') == '1'

    @mock.patch('airqo_monitor.format_data.get_and_format_data_for_channel')
    @mock.patch('airqo_monitor.format_data.get_all_channels_by_type')
    def test_get_and_format_data_for_all_channels(self, get_all_channels_mocker, get_and_format_data_for_channel_mocker):
        get_all_channels_mocker.return_value = [
            dict(name='channel1', id=9999),
            dict(name='channel2', id=8888),
        ]

        entry = {'entry_id': 1, 'latitude': '1', 'longitude': '1'}
        get_and_format_data_for_channel_mocker.return_value = [entry]

        channel_info = get_and_format_data_for_all_channels()
        assert len(channel_info) == 2

        channel1 = Channel.objects.get(name='channel1')
        channel2 = Channel.objects.get(name='channel2')

        assert channel1.channel_id == 9999
        assert channel1.channel_type is not None

        assert channel2.channel_id == 8888
        assert channel2.channel_type is not None

        assert len(channel_info[9999]['data']) == 1
        assert channel_info[9999]['data'][0].get('entry_id') == 1
        assert channel_info[9999]['data'][0].get('latitude') == '1'
        assert channel_info[9999]['data'][0].get('longitude') == '1'

        assert len(channel_info[8888]['data']) == 1
        assert channel_info[8888]['data'][0].get('entry_id') == 1
        assert channel_info[8888]['data'][0].get('latitude') == '1'
        assert channel_info[8888]['data'][0].get('longitude') == '1'
