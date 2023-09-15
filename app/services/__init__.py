from abc import abstractmethod, ABC
from typing import Optional
from app.services.dto.location import Location
from app.services.dto.weather import CurrentWeather, WeatherForecast


class WeatherService(ABC):
    @abstractmethod
    def find_place(self, query: str) -> Optional[Location]:
        pass

    @abstractmethod
    def get_current(self, location: Location) -> CurrentWeather:
        pass

    @classmethod
    def get_forecast(self, location: Location) -> WeatherForecast:
        pass