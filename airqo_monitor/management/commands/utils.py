import json

from airqo_monitor.models import (
    Channel,
    ChannelType,
    GlobalVariable,
    MalfunctionReason,
)
from airqo_monitor.utils import update_last_channel_update_time

def create_basic_test_data():
    # ChannelType
    if not ChannelType.objects.filter(name='airqo').exists():
        channel_type = ChannelType.objects.create(
            name='airqo',
            friendly_name='Airqo',
            data_format_json=json.dumps({"field1": "analog_value", "field2": "sensor_voltage_out", "field3": "VWC", "field4": "H20_percent", "field5": "latitude", "field6": "longitude", "field7": "battery_voltage", "field8": "latlonalt"})
        )

    # Malfunction detection variables
    GlobalVariable.objects.get_or_create(key='LAST_CHANNEL_UPDATE_TIME')
    update_last_channel_update_time()

    low_battery_cutoff, _ = GlobalVariable.objects.get_or_create(key='LOW_BATTERY_CUTOFF')
    low_battery_cutoff.value = '0.3'
    low_battery_cutoff.save()

    airqo_num_reports_to_verify_sensor_malfunction, _ = GlobalVariable.objects.get_or_create(key='AIRQO_NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION')
    airqo_num_reports_to_verify_sensor_malfunction.value = '10'
    airqo_num_reports_to_verify_sensor_malfunction.save()

    airqo_sensor_pm_2_5_min_cutoff, _ = GlobalVariable.objects.get_or_create(key='AIRQO_SENSOR_PM_2_5_MIN_CUTOFF')
    airqo_sensor_pm_2_5_min_cutoff.value = '1.0'
    airqo_sensor_pm_2_5_min_cutoff.save()

    airqo_sensor_pm_2_5_max_cutoff, _ = GlobalVariable.objects.get_or_create(key='AIRQO_SENSOR_PM_2_5_MAX_CUTOFF')
    airqo_sensor_pm_2_5_max_cutoff.value = '1000.0'
    airqo_sensor_pm_2_5_max_cutoff.save()

    airqo_allowable_outlier_sensor_ratio, _ = GlobalVariable.objects.get_or_create(key='AIRQO_ALLOWABLE_OUTLIER_SENSOR_RATIO')
    airqo_allowable_outlier_sensor_ratio.value = '0.2'
    airqo_allowable_outlier_sensor_ratio.save()

    airqo_num_reports_to_verify_reporting_malfunction, _ = GlobalVariable.objects.get_or_create(key='AIRQO_NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION')
    airqo_num_reports_to_verify_reporting_malfunction.value = '10'
    airqo_num_reports_to_verify_reporting_malfunction.save()

    airqo_maximum_average_seconds_between_reports, _ = GlobalVariable.objects.get_or_create(key='AIRQO_MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS')
    airqo_maximum_average_seconds_between_reports.value = '180'
    airqo_maximum_average_seconds_between_reports.save()

    # Malfunction reasons
    MalfunctionReason.objects.get_or_create(name='reporting_outliers')
    MalfunctionReason.objects.get_or_create(name='low_reporting_frequency')
    MalfunctionReason.objects.get_or_create(name='low_battery_voltage')
    MalfunctionReason.objects.get_or_create(name='no_data')
