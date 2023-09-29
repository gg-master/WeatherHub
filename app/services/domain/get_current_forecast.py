import logging
from app.services.domain.contract.usecase_command import UseCaseCommand
from app.services.domain.contract.weather_repository import IWeatherRepository


class GetCurrentForecast(UseCaseCommand):
    def execute(self):
        ...
