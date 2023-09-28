from abc import ABC, abstractmethod

from app.services.domain.dto.location import Location
from app.services.domain.dto.weather import CurrentWeather, WeatherForecast


class IWeatherRepository(ABC):
    @abstractmethod
    def get_current_weather(self, location: Location) -> CurrentWeather:
        raise NotImplementedError

    @abstractmethod
    def get_forecast(self, location: Location) -> WeatherForecast:
        raise NotImplementedError
