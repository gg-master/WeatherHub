from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass
class Location:
    place: str
    country: str
    lat: float
    long: float


class WeatherProvider(Protocol):
    # TODO этот метод должен быть публичным?
    @abstractmethod
    def _find_place(self, query: str) -> Optional[Location]:
        ...

    @abstractmethod
    def get_current(self, location: Location) -> 'CurrentWeather':
        ...

    @abstractmethod
    def get_forecast(self, location: Location) -> 'WeatherForecast':
        ...
