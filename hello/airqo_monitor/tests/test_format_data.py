import mock
import unittest

from datetime import datetime, timedelta

from constants import (
    THINGSPEAK_CHANNELS_LIST_URL,
    THINGSPEAK_FEEDS_LIST_URL,
)
from models.data_entry import DataEntry
from external.thingspeak import (
    get_all_channel_ids,
    get_data_for_channel,
)
from format_data import (
    get_and_format_data_for_all_channels,
    get_and_format_data_for_channel,
)


class TestFormatData(unittest.TestCase):

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

    @mock.patch('format_data.get_data_for_channel')
    def test_get_and_format_data_for_channel(self, get_data_for_channel_mocker):
        get_data_for_channel_mocker.return_value = self.sample_json_entries

        data = get_and_format_data_for_channel(123)
        assert data[0].created_at == '2017-03-26T22:53:55Z'
        assert data[0].channel_id == 123
        assert data[0].entry_id == 1
        assert data[0].pm_1 == '35.00'
        assert data[0].pm_2_5 == '36.00'
        assert data[0].pm_10 == ' 6.30'
        assert data[0].sample_period == ' 3400.07'
        assert data[0].latitude == '172'
        assert data[0].longitude == '1'
        assert data[0].battery_voltage == '16'
        assert data[0].is_mobile is False

        assert data[1].channel_id == 123
        assert data[1].entry_id == 2

        assert data[2].channel_id == 123
        assert data[2].entry_id == 3

    @mock.patch('format_data.get_data_for_channel')
    def test_get_and_format_data_for_channel_with_field8(self, get_data_for_channel_mocker):
        sample_json_entries = self.sample_json_entries
        sample_json_entries[0]['field8'] = '6,7,8,9,10,11'

        get_data_for_channel_mocker.return_value = sample_json_entries

        data = get_and_format_data_for_channel(123)
        assert data[0].created_at == '2017-03-26T22:53:55Z'
        assert data[0].channel_id == 123
        assert data[0].entry_id == 1
        assert data[0].pm_1 == '35.00'
        assert data[0].pm_2_5 == '36.00'
        assert data[0].pm_10 == ' 6.30'
        assert data[0].sample_period == ' 3400.07'
        assert data[0].latitude == '6'
        assert data[0].longitude == '7'
        assert data[0].battery_voltage == '16'
        assert data[0].altitude == '8'
        assert data[0].speed == '9'
        assert data[0].num_satellites == '10'
        assert data[0].hdop == '11'

        assert data[1].channel_id == 123
        assert data[1].entry_id == 2
        assert data[1].altitude is None
        assert data[2].speed is None
        assert data[2].num_satellites is None
        assert data[2].hdop is None

        assert data[2].channel_id == 123
        assert data[2].entry_id == 3
        assert data[2].altitude is None
        assert data[2].speed is None
        assert data[2].num_satellites is None
        assert data[2].hdop is None

    @mock.patch('format_data.get_and_format_data_for_channel')
    @mock.patch('format_data.get_all_channel_ids')
    def test_get_and_format_data_for_all_channels(self, get_all_channel_ids_mocker, get_and_format_data_for_channel_mocker):
        get_all_channel_ids_mocker.return_value = [123, 456]

        entry = DataEntry(channel_id=123, entry_id=1)
        entry.latitude = '1'
        entry.longitude = '1'

        get_and_format_data_for_channel_mocker.return_value = [entry]

        data = get_and_format_data_for_all_channels()
        assert len(data) == 2

        assert len(data[123]) == 1
        assert data[123][0].entry_id == 1
        assert data[123][0].latitude == '1'
        assert data[123][0].longitude == '1'

        assert len(data[456]) == 1
        assert data[456][0].entry_id == 1
        assert data[456][0].latitude == '1'
        assert data[456][0].longitude == '1'
