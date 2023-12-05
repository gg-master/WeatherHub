from dataclasses import dataclass
from app.services.domain.dto.location import Location
import datetime
from typing import List


class WeatherConverter:
    @staticmethod
    def convert_precipitation_values(condition: str):
        if condition[:2] == "01":
            return "000"
        elif condition[:2] == "02":
            return "200"
        elif condition[:2] == "03":
            return "300"
        elif condition[:2] == "04":
            return "400"
        elif condition[:2] == "09":
            return "420"
        elif condition[:2] == "10":
            return "320"
        elif condition[:2] == "11":
            return "440"
        elif condition[:2] == "13":
            return "422"
        elif condition[:2] == "50":
            return "500"

    @staticmethod
    def weather_condition(condition: str):
        condition = int(condition)
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
    wind_gust: float


@dataclass
class DayForecast:
    date: datetime.date
    min_temp: int
    max_temp: int
    wind_speed: int
    wind_direction: int
    humidity: int
    condition: str
    wind_gust: float
    sunrise: datetime.time
    sunset: datetime.time
    # daylength: int
    hourly: List[HourForecast]


@dataclass
class CurrentWeather:
    datetime: datetime.datetime
    temp: int
    feel_temp: int
    condition: str
    humidity: int
    pressure: float
    wind_speed: int
    # wind_gust: int
    wind_direction: int
