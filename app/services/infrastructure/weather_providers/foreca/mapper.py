import asyncio
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
        result = current.to_domain()
        result.location = location
        return result


async def get_forecast(location: Location) -> Optional[DomainWeatherForecast]:
    parser = ForecaParser()
    place = await parser.search_place(location.place)
    if len(place):
        place = place[0]
        parser.place = place
        forecasts = await parser.get_forecast()
        days = []
        hours = []
        for i, forecast in enumerate(forecasts):
            forecasts[i] = forecast.to_domain()
            hours.append(parser.get_hourly(i))
        hours = await asyncio.gather(*hours)
        for i, forecast in enumerate(forecasts):
            forecasts[i].hourly = hours[i]
            for j, hour in enumerate(forecasts[i].hourly):
                forecasts[i].hourly[j] = hour.to_domain()
            days.append(forecasts[i])
        return DomainWeatherForecast("foreca", location, days)
