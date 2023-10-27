from dataclasses import dataclass
import datetime
from typing import List
from app.services.domain.dto.location import Location
from app.services.domain.utils.enums import Direction


class WeatherConverter:
    @staticmethod
    def wind_direction(wind_direction: str):
        winddir = None
        if wind_direction == "N":
            winddir = Direction.N
        elif wind_direction == "S":
            winddir = Direction.S
        elif wind_direction == "NE":
            winddir = Direction.NE
        elif wind_direction == "NW":
            winddir = Direction.NW
        elif wind_direction == "SE":
            winddir = Direction.SE
        elif wind_direction == "SW":
            winddir = Direction.SW
        elif wind_direction == "W":
            winddir = Direction.W
        elif wind_direction == "E":
            winddir = Direction.E
        elif isinstance(wind_direction, int) or wind_direction.isdigit():
            winddir = Direction.from_degrees(int(wind_direction))
        return winddir

    @staticmethod
    def weather_condition(condition: str):
        condition = int(condition[1:])
        cloudness = condition // 100
        precip = condition // 10 % 10
        precip_type = condition % 10
        if cloudness > 4:
            cloudness -= 1
        return cloudness, precip, precip_type


@dataclass
class Place:
    id: str
    address: str
    name: str
    country_name: str
    timezone: str
    lat: float
    long: float

    def to_domain(self) -> Location:
        return Location(self.name, self.country_name, self.lat, self.long)
    

@dataclass
class HourForecast:
    time: datetime.time
    temp: int
    feel_temp: int
    condition: str
    humidity: int
    wind_speed: int
    wind_direction: int
    precipitation: float


@dataclass
class DayForecast:
    date: datetime.date
    min_temp: int
    max_temp: int
    wind_speed: int
    wind_direction: int
    humidity: int
    condition: str
    precipitation: float
    sunrise: datetime.time
    sunset: datetime.time
    daylength: int
    hourly: List[HourForecast]


@dataclass
class CurrentWeather:
    datetime: datetime.datetime
    temp: int
    condition: str
    feel_temp: int
    humidity: int
    pressure: float
    wind_speed: int
    wind_gust: int
    wind_direction: int
    precipitation: float
