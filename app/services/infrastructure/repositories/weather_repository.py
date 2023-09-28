from app.services.domain.dto.location import Location
from app.services.domain.dto.weather import CurrentWeather, WeatherForecast
from app.services.domain.interfaces.weather_repository import IWeatherRepository


class WeatherRepository(IWeatherRepository):
    def get_current_weather(self, location: Location) -> CurrentWeather:
        return super().get_current_weather(location)

    def get_forecast(self, location: Location) -> WeatherForecast:
        return super().get_forecast(location)
