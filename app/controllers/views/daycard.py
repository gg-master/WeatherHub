from dataclasses import dataclass
import datetime
from app.services.domain.dto.weather import Weather as DomainWeather
from app.services.domain.utils.sun import SunPositionService


class Weather:
    def __init__(self, domain_weather, location):
        if not isinstance(domain_weather, DomainWeather):
            raise TypeError("Invalid type, required domain weather")
        self.temp = domain_weather.temp
        self.wind = domain_weather.wind
        self.wind_gust = domain_weather.wind_gust
        self.humidity = round(domain_weather.humidity * 100)
        self.pressure = domain_weather.pressure
        self.condition = domain_weather.condition
        if hasattr(domain_weather, "sun"):
            self.sun = domain_weather.sun
        else:
            self.sun = SunPositionService(location).to_domain(datetime.datetime.now().date())
    


@dataclass
class Card:
    weather: Weather
    source: str
    updated: str