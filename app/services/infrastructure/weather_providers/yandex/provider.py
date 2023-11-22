import asyncio
import datetime
import logging
from typing import List
from bs4 import BeautifulSoup as bs

from app.services.infrastructure.weather_providers.yandex.dto import (
    CurrentWeather,
    DayForecast,
    HourForecast,
    Location,
)

from app.utils.requests import fetch_url, to_dict, to_json


class YandexPogodaProvider:
    _logger = logging.getLogger(__name__)

    CURRENT_URL = "https://yandex.ru/pogoda/ru-RU/?lat={}&lon={}"
    FORECAST_URL = (
        "https://yandex.ru/pogoda/ru-RU/details/day-{}?lat={}&lon={}"
    )

    @classmethod
    async def create_for(cls, location: Location) -> "YandexPogodaProvider":
        self = YandexPogodaProvider()
        self._location = location
        return self

    async def get_current(self):
        self._location: Location
        status, text = await fetch_url(
            self.CURRENT_URL.format(self._location.lat, self._location.long)
        )
        if status != 200:
            self._logger.warn("Couldn't get the current weather page")
            return None
        try:
            soup = bs(text, "lxml")
            div_block = soup.find("div", class_="fact__temp-wrap")

            temp, feel_temp = map(
                lambda x: int(x.text),
                div_block.find_all(
                    "span", class_="temp__value temp__value_with-unit"
                ),
            )
            condition = next(
                filter(
                    lambda x: x.startswith("icon_thumb"),
                    div_block.find("img")["class"],
                )
            )

            div_block = soup.find("div", class_="fact__props")

            wind_block = div_block.find(
                "div", class_="term term_orient_v fact__wind-speed"
            )
            wind_speed = int(wind_block.find("span", class_="wind-speed").text)
            wind_dir = wind_block.find("abbr").text

            hum = int(
                div_block.find(class_="term term_orient_v fact__humidity")
                .find(class_="term__value")
                .text.replace("%", "")
            )

            pressure = float(
                div_block.find(class_="term term_orient_v fact__pressure")
                .find(class_="term__value")
                .text.replace(" мм рт. ст.", "")
            )
            return CurrentWeather(
                datetime=datetime.datetime.now(tz=self._location.timezone),
                temp=temp,
                condition=condition,
                feel_temp=feel_temp,
                humidity=hum,
                pressure=pressure,
                wind_speed=wind_speed,
                wind_direction=wind_dir,
            )

        except AttributeError as e:
            self._logger.error("Error parsing current weather")
            return None

    async def get_forecast(self) -> List[DayForecast]:
        return await asyncio.gather(
            *[self._get_dayforecast(i) for i in range(10)]
        )

    async def _get_hourly(self, day: int):
        self._location: Location
        status, text = await fetch_url(
            self.FORECAST_URL.format(
                day, self._location.lat, self._location.long
            )
        )
        if status != 200:
            self._logger.warn("Couldn't get the weather forecast page")
            return None
        try:
            soup = bs(text, "lxml")
            raw_resp = to_dict(soup.find("script", id="__NEXT_DATA__").text)
            day_weather = raw_resp["props"]["pageProps"][
                "detailsMobileServerData"
            ]["weather"]["forecast"]["days"][day + 1]
            hours: List[HourForecast] = []
            for hour in day_weather["hours"]:
                hours.append(
                    HourForecast(
                        time=datetime.datetime.fromisoformat(
                            hour["time"]
                        ).time(),
                        temp=hour["temperature"],
                        condition=hour["icon"],
                        feel_temp=hour["feelsLike"],
                        pressure=hour["pressure"],
                        wind_speed=hour["windSpeed"],
                        wind_direction=hour["windDirection"],
                        wind_gust=hour["windGust"],
                        uv_index=hour["uvIndex"],
                        humidity=hour["humidity"],
                        visibility=hour["visibility"],
                    )
                )
            return hours
        except (AttributeError, KeyError) as e:
            self._logger.error("Error parsing hourly weather")
            return None

    def _get_daypart_name(self, time: datetime.time) -> str:
        if 12 <= time.hour < 18:
            return "day"
        elif 18 <= time.hour <= 23:
            return "evening"
        elif 0 <= time.hour < 6:
            return "night"
        elif 6 <= time.hour < 12:
            return "morning"

    async def _get_dayforecast(self, day: int) -> DayForecast:
        status, text = await fetch_url(
            self.FORECAST_URL.format(
                day, self._location.lat, self._location.long
            )
        )
        hours = await self._get_hourly(day)
        if status != 200:
            self._logger.warn("Couldn't get the day forecast page")
            return None
        try:
            daypart = self._get_daypart_name(
                datetime.datetime.now(tz=self._location.timezone).time()
            )

            soup = bs(text, "lxml")
            raw_resp = to_dict(soup.find("script", id="__NEXT_DATA__").text)
            day_weather = raw_resp["props"]["pageProps"][
                "detailsMobileServerData"
            ]["weather"]["forecast"]["days"][day + 1]
            return DayForecast(
                date=datetime.datetime.fromisoformat(day_weather["time"]),
                temp=day_weather["parts"][daypart]["temperature"],
                feel_temp=day_weather["parts"][daypart]["feelsLike"],
                wind_speed=day_weather["parts"][daypart]["windSpeed"],
                wind_direction=day_weather["parts"][daypart]["windDirection"],
                humidity=day_weather["parts"][daypart]["humidity"],
                condition=day_weather["parts"][daypart]["icon"],
                sunrise=datetime.datetime.fromtimestamp(
                    int(day_weather["sunriseTimestamp"])
                ),
                sunset=datetime.datetime.fromtimestamp(
                    int(day_weather["sunsetTimestamp"])
                ),
                daylength=round(
                    (
                        int(day_weather["sunsetTimestamp"])
                        - int(day_weather["sunriseTimestamp"])
                    )
                    / 60
                ),
                hourly=hours,
            )
        except (AttributeError, KeyError) as e:
            self._logger.error("Error parsing day weather")
            return None
