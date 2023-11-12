import pytz
from datetime import tzinfo

from dataclasses import dataclass
from timezonefinder import TimezoneFinder


@dataclass
class Location:
    place: str
    country: str
    lat: float
    long: float
    timezone: tzinfo = None

    def __post_init__(self):
        if self.timezone is None:
            tf = TimezoneFinder()
            self.timezone = pytz.timezone(
                tf.timezone_at(lat=self.lat, lng=self.long)
            )

    def __str__(self):
        return f"Location[place={self.place};country={self.country}]"
