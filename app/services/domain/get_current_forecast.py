from typing import List

from app.services.domain.contract.usecase_command import UseCaseCommand
from app.services.domain.dto.location import Location

from app.services.domain.dto.weather import CurrentWeather


class GetCurrentForecast(UseCaseCommand):
    async def execute(self, location: Location) -> List[CurrentWeather]:
        return await self._repository.get_current_weathers(location)
        
