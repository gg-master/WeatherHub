from abc import ABC, abstractmethod
import logging
from app.services.domain.contract.weather_repository import IWeatherRepository


class UseCaseCommand(ABC):
    def __init__(self, repository: IWeatherRepository):
        self._logger = logging.getLogger(__name__)
        self._repository = repository

    @abstractmethod
    def execute(self):
        ...
