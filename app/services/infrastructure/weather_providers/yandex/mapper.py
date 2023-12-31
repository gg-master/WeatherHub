import datetime
import logging
from typing import List

from app.services.domain.dto.conditions import WeatherCondition
from app.services.domain.dto.temperature import Temperature
from app.services.domain.dto.wind import Wind
from app.services.domain.dto.sun import SunPosition
from app.services.domain.dto.weather import (
    CurrentWeather as DomainCurrentWeather,
    WeatherForecast as DomainWeatherForecast,
    DayForecast as DomainDayForecast,
    HourlyForecast as DomainHourlyForecast,
)

from app.services.infrastructure.weather_providers.yandex.dto import (
    CurrentWeather,
    DayForecast,
    HourForecast,
    WeatherConverter as WC,
)


class Mapper:
    _logger = logging.getLogger(__name__)

    @staticmethod
    def current_to_domain(current: CurrentWeather) -> DomainCurrentWeather:
        # Probably a parsing error
        if current is None:
            Mapper._logger.warn(
                "CurrentWeather is None and cant be converted"
            )
            return None
        
        return DomainCurrentWeather(
            provider="yandex.pogoda",
            location=None,
            datetime=current.datetime,
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
            wind_gust=None,
        )

    @staticmethod
    def forecast_to_domain(
        forecast: List[DayForecast],
    ) -> DomainWeatherForecast:
        # Probably a parsing error
        if forecast is None:
            Mapper._logger.warn("Forecast is None and cant be converted")
            return None
        
        days: List[DomainDayForecast] = []
        day: DayForecast
        for day in forecast:

            # Probably a parsing error
            if day is None:
                Mapper._logger.warn(
                    "Some day in Forecast is None and cant be converted"
                )
                continue

            hours: List[DomainHourlyForecast] = []
            hour: HourForecast
            if day.hourly is not None:
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
                            wind_gust=None,
                        )
                    )
            else:
                hours = None
            days.append(
                DomainDayForecast(
                    temp=Temperature(day.temp, day.feel_temp),
                    wind=Wind(
                        day.wind_speed, WC.wind_direction(day.wind_direction)
                    ),
                    humidity=day.humidity * 0.01,
                    pressure=day.pressure,
                    condition=WeatherCondition(
                        *WC.weather_condition(day.condition)
                    ),
                    date=day.date,
                    min_temp=None,
                    hourly=hours,
                    sun=SunPosition(
                        day.date, day.sunrise, day.sunset, day.daylength
                    ),
                    wind_gust=Wind(day.wind_gust, None),
                )
            )
        return DomainWeatherForecast(
            datetime=datetime.datetime.now(datetime.timezone.utc),
            provider="yandex.pogoda",
            location=None,
            days=days,
        )
