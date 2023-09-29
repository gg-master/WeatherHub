from dataclasses import dataclass
import datetime

from typing import Dict, Optional
from app.services.domain.dto.conditions import WeatherCondition
from app.services.domain.dto.location import Location

from app.services.domain.dto.temperature import Temperature
from app.services.domain.dto.wind import Wind


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
