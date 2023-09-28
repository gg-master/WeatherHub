import logging
from app.services.domain.interfaces.weather_repository import IWeatherRepository


class GetCurrentForecast:
    def __init__(self, repository: IWeatherRepository):
        self._logger = logging.getLogger(__name__)
        self._repository = repository
        
    def execute(self):
        ...
