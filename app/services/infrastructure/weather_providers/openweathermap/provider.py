from app.utils.requests import fetch_url, to_dict, to_json
from app.services.infrastructure.weather_providers.openweathermap.dto import *
from app.services.domain.utils.enums import Direction
from typing import List, Optional
import asyncio
import os


class OpenWeatherMapFetcher:
    URL = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units={}"

    @classmethod
    async def create_for(cls, location: Location) -> "OpenWeatherMapFetcher":
        self = OpenWeatherMapFetcher()
        self._place = location
        return self

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place: Place):
        self._place = place

    async def _get_hourly(self, day: int) -> List[HourForecast]:
        status, text = await fetch_url(
            self.URL.format(
                self._place.lat,
                self._place.long,
                os.getenv("OPENWEATHERMAP_KEY"),
                "metric",
            )
        )
        if status != 200:
            return []
        result = []
        json_data = to_dict(text).get("hourly")
        for row in json_data:
            time = datetime.datetime.fromtimestamp(row.get("dt", 0)).time().hour
            time = datetime.time(time)
            temp = round(row.get("temp"))
            feel_temp = round(row.get("feels_like"))
            condition = WeatherConverter.convert_precipitation_values(
                row.get("weather", {})[0].get("icon", {})
            )
            humidity = row.get("humidity")
            wind_speed = round(row.get("wind_speed"), 1)
            wind_direction = Direction.from_degrees(row.get("wind_deg"))
            wind_gust = round(row.get("wind_gust"), 1)
            # precipitation
            weather = HourForecast(
                time,
                temp,
                feel_temp,
                condition,
                humidity,
                wind_speed,
                wind_direction,
                wind_gust,
            )
            result.append(weather)
        return result

    async def get_current(self) -> Optional[CurrentWeather]:
        if not self._place:
            return []
        status, text = await fetch_url(
            self.URL.format(
                self._place.lat,
                self._place.long,
                os.getenv("OPENWEATHERMAP_KEY"),
                "metric",
            )
        )
        if status != 200:
            return None

        json_data = to_dict(text).get("current")
        temp = round(json_data.get("temp"))
        feel_temp = round(json_data.get("feels_like"))
        condition = WeatherConverter.convert_precipitation_values(
            json_data.get("weather", {})[0].get("icon", {})
        )
        humidity = json_data.get("humidity")
        pressure = json_data.get("pressure")
        wind_speed = json_data.get("wind_speed")
        # wind_gust
        wind_direction = Direction.from_degrees(json_data.get("wind_deg"))

        return CurrentWeather(
            datetime.datetime.now(datetime.timezone.utc),
            temp,
            feel_temp,
            condition,
            humidity,
            pressure,
            wind_speed,
            # gust,
            wind_direction,
        )

    async def get_forecast(self) -> List[DayForecast]:
        if not self._place:
            return []
        status, text = await fetch_url(
            self.URL.format(
                self._place.lat,
                self._place.long,
                os.getenv("OPENWEATHERMAP_KEY"),
                "metric",
            )
        )
        if status != 200:
            return []
        result = to_dict(text)["daily"]
        days = []
        hours = await asyncio.gather(*[self._get_hourly(i) for i in range(10)])
        for i, day in enumerate(result):
            day = DayForecast(
                datetime.datetime.fromtimestamp(day["dt"]).date(),
                round(day["temp"]["min"]),
                round(day["temp"]["max"]),
                round(day["wind_speed"], 1),
                day["wind_deg"],
                day["humidity"],
                WeatherConverter.convert_precipitation_values(
                    day.get("weather", {})[0].get("icon", {})
                ),
                round(day["wind_gust"], 1),
                datetime.datetime.fromtimestamp(day["sunrise"]).time(),
                datetime.datetime.fromtimestamp(day["sunset"]).time(),
                # int(day["daylen"]),
                hourly=hours[i] if i < 10 else None,
            )
            days.append(day)
        return days
