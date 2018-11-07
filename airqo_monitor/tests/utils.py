from airqo_monitor.models import GlobalVariable

def create_malfunction_global_vars():
    # airqo vars
    GlobalVariable.objects.create(key='LOW_BATTERY_CUTOFF', value=3.3)
    GlobalVariable.objects.create(key='NUM_REPORTS_TO_VERIFY_SENSOR_MALFUNCTION', value=10)
    GlobalVariable.objects.create(key='SENSOR_PM_2_5_MIN_CUTOFF', value=1.0)
    GlobalVariable.objects.create(key='SENSOR_PM_2_5_MAX_CUTOFF', value=1000.0)
    GlobalVariable.objects.create(key='ALLOWABLE_OUTLIER_SENSOR_RATIO', value=0.2)
    GlobalVariable.objects.create(key='NUM_REPORTS_TO_VERIFY_REPORTING_MALFUNCTION', value=10)
    GlobalVariable.objects.create(key='MAXIMUM_AVERAGE_SECONDS_BETWEEN_REPORTS', value=180)
