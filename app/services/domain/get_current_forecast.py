from typing import List

from app.services.domain.contract.usecase_command import UseCaseCommand
from app.services.domain.dto.location import Location

from app.services.domain.dto.weather import CurrentWeather
from app.utils.cache.cacher import AsyncPickleCacher
from app.utils.cache.collections import CacheableList


class GetCurrentForecast(UseCaseCommand):
    @AsyncPickleCacher(2)
    async def execute(self, location: Location) -> List[CurrentWeather]:
        return CacheableList(await self._repository.get_current_weathers(location))
        
