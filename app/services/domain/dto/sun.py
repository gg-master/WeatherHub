from dataclasses import dataclass
import datetime


@dataclass
class SunPosition:
    day: datetime.date
    sunrise: datetime.time
    sunset: datetime.time
    daylength: int  # minutes
