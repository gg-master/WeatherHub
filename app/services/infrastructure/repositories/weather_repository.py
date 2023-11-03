import asyncio
import logging
from typing import List

from app.services.domain.dto.location import Location
from app.services.domain.dto.weather import CurrentWeather, WeatherForecast
from app.services.domain.contract.weather_repository import IWeatherRepository

from app.services.infrastructure.weather_providers import registered_providers
from app.services.infrastructure.weather_providers.providers_contract import (
    WeatherProvider
)


class WeatherRepository(IWeatherRepository):
    _logger = logging.getLogger(__name__)

    async def _activate_providers(
        self, location: Location
    ) -> List[WeatherProvider]:
        return await asyncio.gather(
            *[
                asyncio.create_task(provider.create_for(location))
                for provider in registered_providers.keys()
            ]
        )

    async def get_current_weathers(
        self, location: Location
    ) -> List[CurrentWeather]:
        providers = await self._activate_providers(location)

        raw_result = await asyncio.gather(
            *[
                asyncio.create_task(provider.get_current())
                for provider in providers
            ]
        )

        return [
            mapper.current_to_domain(raw_result[i])
            for i, mapper in enumerate(registered_providers.values())
        ]

    async def get_forecasts(self, location: Location) -> List[WeatherForecast]:
        providers = await self._activate_providers(location)

        raw_result = await asyncio.gather(
            *[
                asyncio.create_task(provider.get_forecast())
                for provider in providers
            ]
        )

        return [
            mapper.forecast_to_domain(raw_result[i])
            for i, mapper in enumerate(registered_providers.values())
        ]
