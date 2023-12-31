from abc import abstractmethod
from typing import Optional, Protocol
from app.services.domain.dto.location import Location

from app.services.domain.dto.weather import CurrentWeather, WeatherForecast


class WeatherProvider(Protocol):
    @abstractmethod
    async def create_for(self, location: Location) -> "WeatherProvider":
        ...

    @abstractmethod
    async def get_current(self) -> Optional[CurrentWeather]:
        ...

    @abstractmethod
    async def get_forecast(self) -> Optional[WeatherForecast]:
        ...


class ProviderMapper(Protocol):
    @abstractmethod
    def current_to_domain(
        self, current: "CurrentWeather"
    ) -> Optional[CurrentWeather]:
        ...

    @abstractmethod
    def forecast_to_domain(
        self, forecast: "WeatherForecast"
    ) -> Optional[WeatherForecast]:
        ...
