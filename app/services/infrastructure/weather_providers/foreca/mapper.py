import asyncio
from typing import List, Optional

from app.services.domain.dto.conditions import WeatherCondition
from app.services.domain.dto.temperature import Temperature
from app.services.domain.dto.location import Location
from app.services.domain.dto.wind import Wind
from app.services.domain.dto.sun import SunPosition
from app.services.domain.dto.weather import (
    CurrentWeather as DomainCurrentWeather,
    WeatherForecast as DomainWeatherForecast,
    DayForecast as DomainDayForecast,
    HourlyForecast as DomainHourlyForecast,
)

from app.services.infrastructure.weather_providers.foreca.dto import (
    CurrentWeather,
    DayForecast,
    HourForecast,
    WeatherConverter as WC,
)
from app.services.infrastructure.weather_providers.foreca.provider import (
    ForecaParser,
)


class Mapper:
    @staticmethod
    def current_to_domain(current: CurrentWeather) -> DomainCurrentWeather:
        return DomainCurrentWeather(
            provider="foreca",
            location=None,
            date=current.datetime,
            temp=Temperature(current.temp, current.feel_temp),
            wind=Wind(
                current.wind_speed,
                WC.wind_direction(current.wind_direction),
            ),
            humidity=current.humidity * 0.01,
            pressure=current.pressure,
            condition=WeatherCondition(
                *WC.weather_condition(current.condition)
            ),
        )

    @staticmethod
    def forecast_to_domain(
        forecast: List[DayForecast],
    ) -> DomainWeatherForecast:
        days: List[DomainDayForecast] = []
        day: DayForecast
        for day in forecast:
            hours: List[DomainHourlyForecast] = []
            hour: HourForecast
            for hour in day.hourly:
                hours.append(
                    DomainHourlyForecast(
                        temp=Temperature(hour.temp, hour.feel_temp),
                        wind=Wind(
                            hour.wind_speed,
                            WC.wind_direction(hour.wind_direction),
                        ),
                        humidity=hour.humidity * 0.01,
                        pressure=None,
                        condition=WeatherCondition(
                            *WC.weather_condition(hour.condition)
                        ),
                        time=hour.time,
                    )
                )
            days.append(
                DomainDayForecast(
                    temp=Temperature(day.max_temp, None),
                    wind=Wind(
                        day.wind_speed, WC.wind_direction(day.wind_direction)
                    ),
                    humidity=day.humidity * 0.01,
                    pressure=None,
                    condition=WeatherCondition(
                        *WC.weather_condition(day.condition)
                    ),
                    date=day.date,
                    min_temp=Temperature(day.min_temp, None),
                    hourly=hours,
                    sun=SunPosition(
                        day.date, day.sunrise, day.sunset, day.daylength
                    ),
                )
            )
        return DomainWeatherForecast(
            provider="foreca",
            location=None,
            days=days,
        )
