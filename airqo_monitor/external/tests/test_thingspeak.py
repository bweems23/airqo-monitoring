import mock
import unittest

from datetime import datetime, timedelta

from airqo_monitor.constants import (
    THINGSPEAK_CHANNELS_LIST_URL,
    THINGSPEAK_FEEDS_LIST_URL,
)
from airqo_monitor.external.thingspeak import (
    get_all_channels,
    get_api_key_for_channel,
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

    @mock.patch('airqo_monitor.external.thingspeak.make_post_call')
    def test_get_data_for_channel_basic(self, make_post_call_mocker):
        make_post_call_mocker.return_value = self.sample_feeds_list_response

        result = get_data_for_channel(123)

        assert len(result) == 3

    @mock.patch('airqo_monitor.external.thingspeak.make_post_call')
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

    @mock.patch('airqo_monitor.external.thingspeak.make_get_call')
    @mock.patch('airqo_monitor.external.thingspeak.os.environ.get')
    def test_get_all_channels(self, env_var_mocker, make_get_call_mocker):
        make_get_call_mocker.return_value = [dict(id=1, name='AIRQO'), dict(id=2, name='AIRQO')]
        env_var_mocker.return_value = 'test_key'

        channels = get_all_channels()
        assert channels == [{'id': 1, 'name': 'AIRQO'}, {'id': 2, 'name': 'AIRQO'}]

        expected_url = '{}/?api_key=test_key'.format(THINGSPEAK_CHANNELS_LIST_URL)
        make_get_call_mocker.assert_called_once_with(expected_url)

    @mock.patch('airqo_monitor.external.thingspeak.os.environ.get')
    def test_get_api_key_for_channel(self, env_var_mocker):
        env_var_mocker.return_value = 'test_key'
        api_key = get_api_key_for_channel(123)
        assert api_key == 'test_key'

    def test_get_api_key_for_channel_doesnt_crash_if_no_key(self):
        api_key = get_api_key_for_channel(123)
        assert api_key is None
