from dataclasses import dataclass
import datetime
from app.services.domain.dto.location import Location
from app.services.domain.dto.sun import SunPosition
from app.services.domain.dto.temperature import Temperature
from app.services.domain.dto.weather import (
    CurrentWeather as DomainCurrentWeather,
    HourlyForecast as DomainHourlyForecast,
    DayForecast as DomainDayForecast,
    WeatherForecast as DomainWeatherForecast,
)
from app.services.domain.dto.wind import Wind
from app.services.domain.utils.enums import Direction
from app.services.domain.dto.conditions import WeatherCondition


class WeatherConverter:
    def _wind_direction(self):
        winddir = None
        if self.wind_direction == "N":
            winddir = Direction.N
        elif self.wind_direction == "S":
            winddir = Direction.S
        elif self.wind_direction == "NE":
            winddir = Direction.NE
        elif self.wind_direction == "NW":
            winddir = Direction.NW
        elif self.wind_direction == "SE":
            winddir = Direction.SE
        elif self.wind_direction == "SW":
            winddir = Direction.SW
        elif self.wind_direction == "W":
            winddir = Direction.W
        elif self.wind_direction == "E":
            winddir = Direction.E
        elif isinstance(self.wind_direction, int) or self.wind_direction.isdigit():
            winddir = Direction.from_degrees(int(self.wind_direction))
        return winddir

    def _weather_condition(self):
        condition = int(self.condition[1:])
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
class DayForecast(WeatherConverter):
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

    def to_domain(self):
        return DomainDayForecast(
            Temperature(self.max_temp, None),
            Wind(self.wind_speed, self._wind_direction()),
            self.humidity * 0.01,
            None,
            WeatherCondition(*self._weather_condition()),
            self.date,
            Temperature(self.min_temp, None),
            None,
            SunPosition(self.date, self.sunrise, self.sunset, self.daylength),
        )


@dataclass
class HourForecast(WeatherConverter):
    time: datetime.time
    temp: int
    feel_temp: int
    condition: str
    humidity: int
    wind_speed: int
    wind_direction: int
    precipitation: float

    def to_domain(self):
        return DomainHourlyForecast(
            Temperature(self.temp, self.feel_temp),
            Wind(self.wind_speed, self._wind_direction()),
            self.humidity * 0.01,
            None,
            WeatherCondition(*self._weather_condition()),
            self.time,
        )


@dataclass
class CurrentWeather(WeatherConverter):
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

    def to_domain(self):
        return DomainCurrentWeather(
            Temperature(self.temp, self.feel_temp),
            Wind(self.wind_speed, self._wind_direction()),
            self.humidity * 0.01,
            self.pressure,
            WeatherCondition(*self._weather_condition()),
            "foreca",
            None,
            self.datetime,
        )
