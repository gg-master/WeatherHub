import asyncio
from bs4 import BeautifulSoup as bs
from app.services.infrastructure.weather_providers.foreca.dto import *
from typing import List, Optional
from urllib.parse import quote_plus
import dateparser

from app.utils.requests import fetch_url, to_dict


class ForecaParser:
    SEARCH_URL = "https://api.foreca.net/locations/search/{}.json"
    LOCATION_URL = "https://api.foreca.net/locations/{}.json"
    FORECAST_URL = "https://api.foreca.net/data/favorites/{}.json"
    HOURLY_URL = "https://www.foreca.com/{}/{}/hourly?day={}"
    CURRENT_URL = "https://www.foreca.com/{}/{}"

    COORDS_ACCURACY = 1000

    @classmethod
    async def create_for(cls, location: Location) -> "ForecaParser":
        self = ForecaParser()
        self._place = await self._search_place_by_coords(location.lat, location.long)
        return self

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place: Place):
        self._place = place

    async def _get_hourly(self, day: int) -> List[HourForecast]:
        if not self._place:
            return []
        status, text = await fetch_url(
            self.HOURLY_URL.format(self._place.id, self._place.address, day)
        )
        if status != 200:
            return []
        soup = bs(text, "lxml")
        rows = soup.select(".row")[1:]
        result = []
        for row in rows:
            time = int(row.select(".time_24h")[0].text)
            if time == 24:
                time = 0
            time = datetime.time(time)
            symb = (
                list(row.select(".symb")[0].children)[0]["src"]
                .split("/")[-1]
                .replace(".svg", "")
            )
            temp = int(row.select(".temp_c")[0].text)
            feels_like = int(row.select(".temp_c")[1].text)
            hum = int(row.select(".humidity")[0].text[:-1])
            rain = float(
                row.select(".rain_mm")[0]
                .text.replace(" mm", "")
                .replace(" cm", "")
                .strip()
            )
            wind_dir = list(row.select(".wind")[0].children)[0]["alt"]
            wind_speed = int(row.select(".wind_ms")[0].text)
            weather = HourForecast(
                time, temp, feels_like, symb, hum, wind_speed, wind_dir, rain
            )
            result.append(weather)
        return result

    async def _search_place_by_coords(self, lat, long):
        status, text = await fetch_url(
            self.LOCATION_URL.format(f"{long},{lat}"),
            params={"accuracy": self.COORDS_ACCURACY},
        )
        if status != 200:
            return
        place = to_dict(text)
        address = [
            place.get("defaultName", "").replace(" ", "-"),
            place.get("admName", "").replace(" ", "-"),
            place.get("defaultCountryName", "").replace(" ", "-"),
        ]
        if "" in address:
            address.remove("")
        address = "-".join(address)
        return Place(
            place["id"],
            address,
            place["name"],
            place["countryName"],
            place["timezone"],
            place["lat"],
            place["lon"],
        )

    async def _search_place(self, city_query) -> List[Place]:
        status, text = await fetch_url(
            self.SEARCH_URL.format(quote_plus(city_query)),
            params={"limit": 30, "lang": "ru"},
        )
        if status == 200:
            result = to_dict(text)
            places = []
            for place in result["results"]:
                address = [
                    place.get("defaultName", "").replace(" ", "-"),
                    place.get("defaultAdmName", "").replace(" ", "-"),
                    place.get("defaultCountryName", "").replace(" ", "-"),
                ]
                if "" in address:
                    address.remove("")
                address = "-".join(address)
                place = Place(
                    place["id"],
                    address,
                    place["name"],
                    place["countryName"],
                    place["timezone"],
                    place["lat"],
                    place["lon"],
                )
                places.append(place)
            return places
        return []

    async def get_current(self) -> Optional[CurrentWeather]:
        if not self._place:
            return []
        status, text = await fetch_url(
            self.CURRENT_URL.format(self._place.id, self._place.address)
        )
        if status != 200:
            return None
        soup = bs(text, "lxml")
        row = soup.select(".row")[0]

        symb = (
            list(row.select(".symb")[0].children)[0]["src"]
            .split("/")[-1]
            .replace(".svg", "")
        )
        temp = int(row.select(".temp_c")[0].text[:-1])
        feels_like = int(row.select(".temp_c")[1].text[:-1])
        wind_dir = list(row.select(".wind")[0].children)[0]["alt"]
        wind_speed = int(row.select(".wind_ms")[0].text.replace(" m/s", ""))
        gust = int(row.select(".wind_ms")[1].text.replace(" m/s", ""))

        row = soup.select(".row.details")[0]
        hum = int(row.select(".rhum")[0].select("em")[0].text)
        rain = float(row.select(".rain_mm")[0].text.replace(" mm", ""))
        pressure = float(row.select(".pres_mmhg")[0].select("em")[0].text)

        return CurrentWeather(
            datetime.datetime.now(datetime.timezone.utc),
            temp,
            symb,
            feels_like,
            hum,
            pressure,
            wind_speed,
            gust,
            wind_dir,
            rain,
        )

    async def get_forecast(self) -> List[DayForecast]:
        if not self._place:
            return []
        status, text = await fetch_url(self.FORECAST_URL.format(self._place.id))
        if status != 200:
            return []
        result = to_dict(text)[self._place.id]
        days = []
        hours = await asyncio.gather(*[self._get_hourly(i) for i in range(10)])
        for i, day in enumerate(result[:10]):
            day = DayForecast(
                dateparser.parse(day["date"]).date(),
                day["tmin"],
                day["tmax"],
                day["winds"],
                day["windd"],
                day["rhum"],
                day["symb"],
                day["rain"],
                dateparser.parse(day["sunrise"]).time(),
                dateparser.parse(day["sunset"]).time(),
                int(day["daylen"]),
                hourly=hours[i] if i < 10 else None,
            )
            days.append(day)
        return days
