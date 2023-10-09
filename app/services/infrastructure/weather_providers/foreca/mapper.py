from typing import Optional

from app.services.domain.dto.weather import (
    CurrentWeather as DomainCurrentWeather,
    WeatherForecast as DomainWeatherForecast,
)
from app.services.domain.dto.location import Location
from app.services.infrastructure.weather_providers.foreca.provider import ForecaParser


async def get_current(location: Location) -> Optional[DomainCurrentWeather]:
    parser = ForecaParser()
    place = await parser.search_place(location.place)
    if len(place):
        place = place[0]
        parser.place = place
        current = await parser.get_current()
        return current.to_domain()


async def get_forecast(location: Location) -> Optional[DomainWeatherForecast]:
    parser = ForecaParser()
    place = await parser.search_place(location.place)
    if len(place):
        place = place[0]
        parser.place = place
        forecasts = await parser.get_forecast()
        days = {}
        for i, forecast in enumerate(forecasts):
            date = forecast.date
            forecasts[i] = forecast.to_domain()
            forecasts[i].hourly = await parser.get_hourly(i)
            days[date] = forecasts[i]
        return DomainWeatherForecast("foreca", location, days)
