from dataclasses import dataclass
from app.services.domain.dto.location import Location
import datetime
from typing import List

class WeatherConverter:
    @staticmethod
    def convert_precipitation_values(condition: int):
        if condition // 100 in [2, 3]:
            if condition % 10 == 0:
                return '10'
            elif condition % 10 == 1:
                return '20'
            elif condition % 10 == 2:
                return '30'
        elif condition // 100 == 5:
            if condition % 10 == 0:
                return '10'
            elif condition % 10 == 1:
                return '20'
            elif condition % 10 == 2:
                return '30'
            elif condition % 10 == 3:
                return '40'
        elif condition // 100 == 6:
            if condition % 10 == 0:
                return '12'
            elif condition % 10 == 1:
                return '22'
            elif condition % 10 == 2:
                return '32'
            elif condition % 10 == 6:
                return '32'

        elif condition // 100 in [7, 8]:
            return '00'

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
    #daylength: int
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
    #wind_gust: int
    wind_direction: int