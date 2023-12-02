from app.utils.requests import fetch_url, to_dict, to_json
from app.services.infrastructure.weather_providers.openweathermap.dto import *
from app.services.domain.utils.enums import Direction
from typing import List, Optional
import asyncio
import os

class OpenWeatherMapFetcher:
    URL = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units={}'

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
            self.URL.format(self._place.lat, self._place.long, os.getenv("OPENWEATHERMAP_KEY"), 'metric')
        )
        if status != 200:
            return []
        result = []
        json_data = to_dict(text).get("hourly")
        for row in json_data:
            time = datetime.datetime.fromtimestamp(row.get("dt", 0)).time().hour
            time = datetime.time(time)
            temp = row.get("temp")
            feel_temp = row.get("feels_like")
            condition = str(int(row.get("clouds", 0) / 20)) + WeatherConverter.convert_precipitation_values(
                row.get("weather", {})[0].get("id", {}))
            humidity = row.get("humidity")
            wind_speed = row.get("wind_speed")
            wind_direction = Direction.from_degrees(row.get("wind_deg"))
            wind_gust = row.get("wind_gust")
            # precipitation
            weather = HourForecast(
                time, temp, feel_temp, condition, humidity, wind_speed, wind_direction, wind_gust
            )
            result.append(weather)
        return result

    async def get_current(self) -> Optional[CurrentWeather]:
        if not self._place:
            return []
        status, text = await fetch_url(
            self.URL.format(self._place.lat, self._place.long, os.getenv("OPENWEATHERMAP_KEY"), 'metric')
        )
        if status != 200:
            return None

        json_data = to_dict(text).get("current")
        temp = json_data.get("temp")
        feel_temp = json_data.get("feels_like")
        condition = str(int(json_data.get("clouds", 0) / 20)) + WeatherConverter.convert_precipitation_values(
            json_data.get("weather", {})[0].get("id", {}))
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
            #gust,
            wind_direction,
        )

    async def get_forecast(self) -> List[DayForecast]:
        if not self._place:
            return []
        status, text = await fetch_url(self.URL.format(self._place.lat, self._place.long, os.getenv("OPENWEATHERMAP_KEY"), 'metric'))
        if status != 200:
            return []
        result = to_dict(text)["daily"]
        days = []
        hours = await asyncio.gather(*[self._get_hourly(i) for i in range(10)])
        for i, day in enumerate(result):
            day = DayForecast(
                datetime.datetime.fromtimestamp(day["dt"]).date(),
                day["temp"]["min"],
                day["temp"]["max"],
                day["wind_speed"],
                day["wind_deg"],
                day["humidity"],
                str(int(day.get("clouds", 0) / 20)) + WeatherConverter.convert_precipitation_values(
                    day.get("weather", {})[0].get("id", {})),
                day["wind_gust"],
                datetime.datetime.fromtimestamp(day["sunrise"]).time(),
                datetime.datetime.fromtimestamp(day["sunset"]).time(),
                #int(day["daylen"]),
                hourly=hours[i] if i < 10 else None,
            )
            days.append(day)
        return days
