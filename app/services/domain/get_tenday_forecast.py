from typing import List

from app.services.domain.contract.usecase_command import UseCaseCommand
from app.services.domain.dto.location import Location

from app.services.domain.dto.weather import WeatherForecast
from app.services.infrastructure.repositories import WeatherRepository
from app.utils.cache.cacher import AsyncPickleCacher
from app.utils.cache.collections import CacheableList


class GetTendayForecast(UseCaseCommand):
    @AsyncPickleCacher(2)
    async def execute(self, location: Location) -> List[WeatherForecast]:
        return CacheableList(await self._repository.get_forecasts(location))
        