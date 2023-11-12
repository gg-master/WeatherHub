from dataclasses import dataclass
from datetime import datetime
from typing import List
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
        hourly: List[HourlyForecast],
        location: Location,
        source: str,
    ) -> None:
        self._source: str = source
        self._date = date
        self._hourly: List[HourlyForecast] = hourly
        self._sun_service = SunPositionService(location)

    @property
    def source(self) -> str:
        return self._source

    @property
    def hourly(self) -> WeatherView:
        forecast: HourlyForecast
        for forecast in self._hourly:
            yield self.WeatherView(
                **forecast.__dict__,
                condition_image=self._get_condition_image(forecast),
            )

    def _get_condition_image(self, forecast: HourlyForecast) -> str:
        local_datetime = self._date.replace(
            hour=forecast.time.hour, minute=forecast.time.minute
        )
        image_name = (
            "d" if self._sun_service.is_daytime(local_datetime) else "n"
        )

        if forecast.condition.cloudness == 5:
            image_name += "6"
        else:
            image_name += str(forecast.condition.cloudness)

        image_name += str(forecast.condition.precipitation)
        image_name += str(forecast.condition._precipitation_type)

        return f"img/foreca_conditions/{image_name}.png"
