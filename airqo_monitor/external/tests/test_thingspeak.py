import mock
import unittest

from datetime import datetime, timedelta

from constants import (
    THINGSPEAK_CHANNELS_LIST_URL,
    THINGSPEAK_FEEDS_LIST_URL,
)
from external.thingspeak import (
    get_all_channel_ids,
    get_data_for_channel,
)


class TestThingspeakAPI(unittest.TestCase):

    sample_feeds_list_response = {
        'channel': [],
        'feeds':
            [
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
                    u'field2': u'36.00',
                    u'field3': u' 6.30',
                    u'created_at': u'2017-03-27T22:53:55Z',
                    u'field1': u'35.00',
                    u'field6': u'1',
                    u'field7': u'16',
                    u'field4': u' 3400.07',
                    u'field5': u'172',
                    u'entry_id': 1
                },
                {
                    u'field2': u'36.00',
                    u'field3': u' 6.30',
                    u'created_at': u'2017-03-28T22:53:55Z',
                    u'field1': u'35.00',
                    u'field6': u'1',
                    u'field7': u'16',
                    u'field4': u' 3400.07',
                    u'field5': u'172',
                    u'entry_id': 1
                },
            ]
    }

    @mock.patch('external.thingspeak.make_post_call')
    def test_get_data_for_channel_basic(self, make_post_call_mocker):
        make_post_call_mocker.return_value = self.sample_feeds_list_response

        result = get_data_for_channel(123)

        assert len(result) == 3

    @mock.patch('external.thingspeak.make_post_call')
    def test_get_data_for_channel_with_times(self, make_post_call_mocker):
        make_post_call_mocker.return_value = self.sample_feeds_list_response

        start_time = datetime.now() - timedelta(hours=5)
        start_time_string = datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%SZ')

        end_time = datetime.now()
        end_time_string = datetime.strftime(end_time,'%Y-%m-%dT%H:%M:%SZ')

        result = get_data_for_channel(123, start_time=start_time, end_time=end_time)

        assert len(result) == 3
        make_post_call_mocker.assert_called_once_with('{}/feeds/?start={}&end={}'.format(
            THINGSPEAK_FEEDS_LIST_URL.format('123'),
            start_time_string,
            end_time_string
        ))

    @mock.patch('external.thingspeak.make_get_call')
    def test_get_all_channel_ids(self, make_get_call_mocker):
        make_get_call_mocker.return_value = {
            "channels": [dict(id=1, name='AIRQO'), dict(id=2, name='AIRQO')]
        }

        channels = get_all_channel_ids()
        assert channels == [1, 2]

        make_get_call_mocker.assert_called_once_with(THINGSPEAK_CHANNELS_LIST_URL)

    @mock.patch('external.thingspeak.make_get_call')
    def test_get_all_channel_ids_filters_correct_channels(self, make_get_call_mocker):
        make_get_call_mocker.return_value = {
            "channels": [
                dict(id=1, name='AIRQO Test - ACTIVE'),
                dict(id=2, name='AIRQO Test - INACTIVE'),
                dict(id=3, name='Test - ACTIVE'),
                dict(id=4, name='Test - INACTIVE'),
            ]
        }

        channels = get_all_channel_ids()
        assert channels == [1]

        make_get_call_mocker.assert_called_once_with(THINGSPEAK_CHANNELS_LIST_URL)
