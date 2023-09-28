from app.services.dto.temperature import Temperature
from app.services.dto.wind import Wind
from app.services.dto.location import Location
from app.services.dto.conditions import WeatherCondition

from dataclasses import dataclass
import datetime

from typing import Dict, Optional


@dataclass
class Weather:
    temp: Temperature
    wind: Wind
    humidity: float
    pressure: float
    condition: WeatherCondition

@dataclass
class CurrentWeather(Weather):
    provider: str
    location: Location
    date: datetime.datetime


@dataclass
class HourlyForecast(Weather):
    time: datetime.time


@dataclass
class DayForecast(Weather):
    min_temp: Temperature
    hourly: Optional[HourlyForecast]


@dataclass
class WeatherForecast(Weather):
    provider: str
    location: Location
    days: Dict[datetime.date, DayForecast]