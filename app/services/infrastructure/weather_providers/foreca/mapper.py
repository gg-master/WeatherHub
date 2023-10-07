from typing import Optional

from app.services.domain.dto.sun import SunPosition
from app.services.domain.dto.weather import (
    CurrentWeather as DomainCurrentWeather,
    WeatherForecast as DomainWeatherForecast,
)
from app.services.domain.dto.location import Location
from app.services.infrastructure.weather_providers.foreca.provider import ForecaParser


def get_current(location: Location) -> Optional[DomainCurrentWeather]:
    parser = ForecaParser()
    place = parser.search_place(location.place)
    if len(place):
        place = place[0]
        parser.place = place
        current = parser.get_current()
        return current.to_domain()


def get_forecast(location: Location) -> Optional[DomainWeatherForecast]:
    parser = ForecaParser()
    place = parser.search_place(location.place)
    if len(place):
        place = place[0]
        parser.place = place
        forecasts = parser.get_forecast()
        days = {}
        for i, forecast in enumerate(forecasts):
            date = forecast.date
            forecasts[i] = forecast.to_domain()
            forecasts[i].hourly = parser.get_hourly(i)
            days[date] = forecasts[i]
        return DomainWeatherForecast("foreca", location, days)


def get_sun_position(location: Location):
    parser = ForecaParser()
    place = parser.search_place(location.place)
    if len(place):
        place = place[0]
        parser.place = place
        positions = []
        forecasts = parser.get_forecast()
        for forecast in forecasts:
            positions.append(
                SunPosition(
                    forecast.date, forecast.sunrise, forecast.sunset, forecast.daylength
                )
            )
        return positions
