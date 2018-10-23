###### Thingspeak API ######

# feeds
DEFAULT_THINGSPEAK_FEEDS_INTERVAL_DAYS = 7
THINGSPEAK_FEEDS_LIST_MAX_NUM_RESULTS = 8000
THINGSPEAK_FEEDS_LIST_URL = 'http://thingspeak.com/channels/{}'

# channels
THINGSPEAK_CHANNELS_LIST_URL_TEMPLATE = 'https://api.thingspeak.com/users/{}/channels.json'
MATHWORKS_USER_ID = 'baurd'
THINGSPEAK_CHANNELS_LIST_URL = THINGSPEAK_CHANNELS_LIST_URL_TEMPLATE.format(MATHWORKS_USER_ID)
AIR_QUALITY_MONITOR_KEYWORD = 'AIRQO'
INACTIVE_MONITOR_KEYWORD = 'INACTIVE'
API_KEY_CONFIG_VAR_NAME = 'CHANNEL_{}_API_KEY'

# Constant values used to determine malfunctions.
LOW_BATTERY_CUTOFF = 3.5

NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION = 10
SENSOR_PM_2_5_MIN_CUTOFF = 1.0
SENSOR_PM_2_5_MAX_CUTOFF = 1000.0
ALLOWABLE_OUTLIER_SENSOR_RATIO = 0.2

NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION = 10
MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS = 120
