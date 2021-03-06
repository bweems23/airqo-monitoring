import json, requests
import os

from collections import defaultdict
from datetime import datetime, timedelta
from werkzeug.contrib.cache import SimpleCache

from airqo_monitor.constants import (
    AIR_QUALITY_MONITOR_KEYWORD,
    API_KEY_CONFIG_VAR_NAME,
    DEFAULT_THINGSPEAK_FEEDS_INTERVAL_DAYS,
    INACTIVE_MONITOR_KEYWORD,
    THINGSPEAK_FEEDS_LIST_MAX_NUM_RESULTS,
    THINGSPEAK_CHANNELS_LIST_URL,
    THINGSPEAK_FEEDS_LIST_URL,
)

cache = SimpleCache()


def get_api_key_for_channel(channel_id):
    """
    Get API key for channel from environment variables. They are stored as
    'CHANNEL_<Thingspeak Channel ID>_API_KEY'.

    Returns: string API key for channel
    """
    var_name = API_KEY_CONFIG_VAR_NAME.format(str(channel_id))
    api_key = os.environ.get(var_name)
    return api_key


def get_data_for_channel(channel, start_time=None, end_time=None):
    """
    Get all channel data for a single channel between start_time and end_time. By default,
    the window goes back 1 week.

    This API returns a maximum of 8000 results, so we keep requesting data until we have fewer
    that 8000 results returned, or until we get a -1 response from the API (which means that there are no more results)

    Returns: A list of data point dicts, from oldest to newest
    """
    if not start_time:
        start_time = datetime.now() - timedelta(days=DEFAULT_THINGSPEAK_FEEDS_INTERVAL_DAYS)
    if not end_time:
        end_time = datetime.now()

    # convert to string before the loop because this never changes
    start_time_string = datetime.strftime(start_time,'%Y-%m-%dT%H:%M:%SZ')

    api_url = THINGSPEAK_FEEDS_LIST_URL.format(channel)
    all_data = []

    while start_time <= end_time:
        full_url = '{}/feeds/?start={}&end={}'.format(
            api_url,
            start_time_string,
            datetime.strftime(end_time,'%Y-%m-%dT%H:%M:%SZ'),
        )
        api_key = get_api_key_for_channel(channel)
        if api_key:
            full_url += '&api_key={}'.format(api_key)
        result = make_post_call(full_url)

        # This means we got an empty result set and are done
        if result == -1:
            break

        feeds = result['feeds']
        all_data = feeds + all_data

        # If we aren't hitting the max number of results then we
        # have all of them for the time range and can stop iterating
        if len(feeds) < THINGSPEAK_FEEDS_LIST_MAX_NUM_RESULTS:
            break

        first_result = feeds[0]
        end_time = datetime.strptime(first_result['created_at'],'%Y-%m-%dT%H:%M:%SZ') - timedelta(seconds=1)

    return all_data


def get_all_channels():
    """
    Get all channels from Thingspeak that are associated with our THINGSPEAK_USER_API_KEY

    Returns: List of channel data dicts
    """
    api_key = os.environ.get('THINGSPEAK_USER_API_KEY')
    full_url = '{}/?api_key={}'.format(THINGSPEAK_CHANNELS_LIST_URL, api_key)
    channels = make_get_call(full_url)
    return channels


def get_all_channels_cached():
    """
    Wrapper around get_all_channels to allow caching. This data shouldn't change often.

    Returns: List of channel data dicts
    """
    cached_value = cache.get('get-all-channels')
    if cached_value is None:
        cached_value = get_all_channels()
        cache.set('get-all-channels', cached_value, timeout=30 * 60)
    return cached_value


def get_all_channels_by_type(channel_type):
    """
    Get all channels from Thingspeak that are associated with our THINGSPEAK_USER_API_KEY and
    that have a tag that matches the channel_type param (current types are 'airqo' or 'soil')

    Returns: List of channel data dicts
    """
    api_key = os.environ.get('THINGSPEAK_USER_API_KEY')
    full_url = '{}/?api_key={}&tag={}'.format(THINGSPEAK_CHANNELS_LIST_URL, api_key, channel_type)
    channels = make_get_call(full_url)

    # For some reason the API returns a list on success and a dict when there's an error
    status = channels.get('status') if isinstance(channels, dict) else None
    if status and status != '200':
        print('[get_all_channels_by_type] Problem reaching Thingspeak API with status: {}'.format(status))

    return channels


def make_post_call(url):
    """
    Make a post call to any URL and parse the json

    Returns: Parsed json response (can be dict or list depending on the expected API response)
    """
    return json.loads(requests.post(url).content)


def make_get_call(url):
    """
    Make a get call to any URL and parse the json

    Returns: Parsed json response (can be dict or list depending on the expected API response)
    """
    return json.loads(requests.get(url).content)
