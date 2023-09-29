from abc import ABC, abstractmethod
from typing import List

from app.services.domain.dto.location import Location
from app.services.domain.dto.weather import CurrentWeather, WeatherForecast


class IWeatherRepository(ABC):
    @abstractmethod
    def get_current_weathers(self, location: Location) -> List[CurrentWeather]:
        raise NotImplementedError

    @abstractmethod
    def get_forecasts(self, location: Location) -> List[WeatherForecast]:
        raise NotImplementedError
