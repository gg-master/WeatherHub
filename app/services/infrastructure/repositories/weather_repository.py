from typing import List
from app.services.domain.dto.location import Location
from app.services.domain.dto.weather import CurrentWeather, WeatherForecast
from app.services.domain.contract.weather_repository import IWeatherRepository


class WeatherRepository(IWeatherRepository):
    def get_current_weathers(self, location: Location) -> List[CurrentWeather]:
        ...

    def get_forecasts(self, location: Location) -> List[WeatherForecast]:
        ...
