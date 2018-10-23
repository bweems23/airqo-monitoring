class DataEntry(object):

    def __init__(self, channel_id, entry_id, created_at=None, pm_1=None, pm_2_5=None, pm_10=None, sample_period=None,
                 latitude=None, longitude=None, battery_voltage=None, elevation=None):
        self.created_at = created_at
        self.channel_id = channel_id
        self.entry_id = entry_id
        self.pm_1 = pm_1
        self.pm_2_5 = pm_2_5
        self.pm_10 = pm_10
        self.sample_period = sample_period
        self.latitude = latitude
        self.longitude = longitude
        self.battery_voltage = battery_voltage
        self.elevation = elevation


    created_at = None
    channel_id = None
    entry_id = None
    pm_1 = None
    pm_2_5 = None
    pm_10 = None
    sample_period = None
    latitude = None
    longitude = None
    battery_voltage = None
    altitude = None  # meters
    speed = None  # mps
    num_satellites = None
    hdop = None  # horizontal dilution of precision
    is_mobile = None
