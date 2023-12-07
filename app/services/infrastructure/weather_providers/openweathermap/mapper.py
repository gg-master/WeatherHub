from app.services.domain.dto.weather import (
    CurrentWeather as DomainCurrentWeather,
    WeatherForecast as DomainWeatherForecast,
    DayForecast as DomainDayForecast,
    HourlyForecast as DomainHourlyForecast,
)
from app.services.infrastructure.weather_providers.openweathermap.dto import (
    CurrentWeather,
    HourForecast,
    WeatherConverter as WC,
    DayForecast,
)
from app.services.domain.dto.temperature import Temperature
from app.services.domain.dto.wind import Wind
from app.services.domain.dto.conditions import WeatherCondition
from app.services.domain.utils.enums import Direction
from typing import List
import datetime
from app.services.domain.dto.sun import SunPosition

class Mapper:
    @staticmethod
    def current_to_domain(current: CurrentWeather) -> DomainCurrentWeather:
        if not current:
            return
        return DomainCurrentWeather(
            provider="openweathermap",
            location=None,
            datetime=current.datetime,
            temp=Temperature(current.temp, current.feel_temp),
            wind=Wind(
                current.wind_speed,
                current.wind_direction,
            ),
            humidity=current.humidity * 0.01,
            pressure=current.pressure,
            condition=WeatherCondition(*WC.weather_condition(current.condition)),
            wind_gust=None,
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
            if day.hourly is not None:
                for hour in day.hourly:
                    hours.append(
                        DomainHourlyForecast(
                            temp=Temperature(hour.temp, hour.feel_temp),
                            wind=Wind(
                                hour.wind_speed,
                                hour.wind_direction,
                            ),
                            humidity=hour.humidity * 0.01,
                            pressure=None,
                            condition=WeatherCondition(
                                *WC.weather_condition(hour.condition)
                            ),
                            time=hour.time,
                            wind_gust=Wind(hour.wind_gust, hour.wind_direction),
                        )
                    )
            else:
                hours = None
            daylength = (day.sunset.hour * 60 + day.sunset.minute) - (day.sunrise.hour * 60 + day.sunrise.minute)
            days.append(
                DomainDayForecast(
                    temp=Temperature(day.max_temp, None),
                    wind=Wind(day.wind_speed, Direction.from_degrees(day.wind_direction)),
                    humidity=day.humidity * 0.01,
                    pressure=None,
                    condition=WeatherCondition(*WC.weather_condition(day.condition)),
                    wind_gust=Wind(day.wind_gust, Direction.from_degrees(day.wind_direction)),
                    date=day.date,
                    min_temp=Temperature(day.min_temp, None),
                    hourly=hours,
                    sun=SunPosition(day.date, day.sunrise, day.sunset, daylength)
                )
            )
        return DomainWeatherForecast(
            datetime=datetime.datetime.now(datetime.timezone.utc),
            provider="openweathermap",
            location=None,
            days=days,
        )
