from dataclasses import dataclass
import datetime

from typing import Dict, Optional, List
from app.services.domain.dto.conditions import WeatherCondition
from app.services.domain.dto.location import Location
from app.services.domain.dto.sun import SunPosition

from app.services.domain.dto.temperature import Temperature
from app.services.domain.dto.wind import Wind


@dataclass
class Weather:
    temp: Temperature
    wind: Wind
    humidity: float  # in range [0;1]
    pressure: Optional[float]  # mmHg
    condition: WeatherCondition
    wind_gust: Wind


@dataclass
class CurrentWeather(Weather):
    provider: str
    location: Location
    datetime: datetime.datetime


@dataclass
class HourlyForecast(Weather):
    time: datetime.time


@dataclass
class DayForecast(Weather):
    date: datetime.date
    min_temp: Temperature
    hourly: Optional[HourlyForecast]
    sun: SunPosition


@dataclass
class WeatherForecast:
    datetime: datetime.datetime
    provider: str
    location: Location
    days: List[DayForecast]
