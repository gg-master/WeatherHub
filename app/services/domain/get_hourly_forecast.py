from typing import List

from app.services.domain.contract.usecase_command import UseCaseCommand
from app.services.domain.dto.location import Location

from app.services.domain.dto.weather import WeatherForecast


class GetHourlyForecast(UseCaseCommand):
    async def execute(self, location: Location) -> List[WeatherForecast]:
        # TODO нужно ли возвращать только почасовой?
        return await self._repository.get_forecasts(location)
        