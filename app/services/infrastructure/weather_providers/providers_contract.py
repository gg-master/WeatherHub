from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Protocol, Any
from app.services.domain.dto.location import Location

from app.services.domain.dto.weather import CurrentWeather, WeatherForecast


class WeatherProvider(Protocol):
    @abstractmethod
    async def create_for(self, location: Location) -> Optional[Location]:
        ...

    @abstractmethod
    async def get_current(self) -> 'CurrentWeather':
        ...

    @abstractmethod
    async def get_forecast(self) -> 'WeatherForecast':
        ...


class ProviderMapper(Protocol):
    @abstractmethod
    def current_to_domain(self, current: 'CurrentWeather') -> CurrentWeather:
        ...

    @abstractmethod
    def forecast_to_domain(
        self, forecast: 'WeatherForecast'
    ) -> WeatherForecast:
        ...
