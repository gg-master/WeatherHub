from app.services.infrastructure.weather_providers.providers_contract import (
    Location,
)
from app.services.infrastructure.weather_providers.yandex.yandex_dto import (
    CurrentWeather,
    Forecast,
)


class YandexPogodaProvider:
    def get_current_weather(self, location: Location) -> CurrentWeather:
        pass

    def get_forecast(self, location: Location) -> Forecast:
        pass
