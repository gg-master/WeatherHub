from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from app.services.domain.dto.location import Location
from app.services.domain.dto.weather import HourlyForecast
from app.services.domain.utils.sun import SunPositionService


class HourlyCard:
    @dataclass
    class WeatherView(HourlyForecast):
        condition_image: str

    def __init__(
        self,
        date: datetime,
        updated: datetime,
        hourly: List[HourlyForecast],
        location: Location,
        source: str,
    ) -> None:
        self._source: str = source
        self._date = date
        self._updated = updated
        self._hourly = hourly
        self._sun_service = SunPositionService(location)

    @property
    def source(self) -> str:
        return self._source

    def justify_by_min_hour(self, min_hour):
        hourly = self._hourly
        self._hourly: List[Optional[HourlyForecast]] = [None for i in range(24)]
        for hour in hourly:
            self._hourly[hour.time.hour] = hour
        self._hourly = self._hourly[min_hour:]

    @property
    def updated(self) -> datetime:
        return self._updated

    @property
    def hourly(self) -> WeatherView:
        forecast: Optional[HourlyForecast]
        for forecast in self._hourly:
            if forecast is None:
                yield None
            else:
                yield self.WeatherView(
                    **forecast.__dict__,
                    condition_image=self._get_condition_image(forecast),
                )

    def _get_condition_image(self, forecast: HourlyForecast) -> str:
        local_datetime = self._date.replace(
            hour=forecast.time.hour, minute=forecast.time.minute
        )
        image_name = "d" if self._sun_service.is_daytime(local_datetime) else "n"

        if forecast.condition.cloudness == 5:
            image_name += "6"
        else:
            image_name += str(forecast.condition.cloudness)

        image_name += str(forecast.condition.precipitation)
        image_name += str(forecast.condition.precipitation_type)

        return f"img/foreca_conditions/{image_name}.png"
