import requests
from bs4 import BeautifulSoup as bs
from app.services.infrastructure.weather_providers.foreca.dto import *
from typing import List
from urllib.parse import quote_plus
import dateparser


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class ForecaParser:
    SEARCH_URL = "https://api.foreca.net/locations/search/{}.json"
    FORECAST_URL = "https://api.foreca.net/data/favorites/{}.json"
    HOURLY_URL = "https://www.foreca.com/{}/{}/hourly?day={}"
    CURRENT_URL = "https://www.foreca.com/{}/{}"

    def __init__(self):
        self._place = None

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place: Place):
        self._place = place

    def get_hourly(self, day: int) -> List[HourForecast]:
        r = requests.get(
            self.HOURLY_URL.format(self._place.id, self._place.address, day),
            headers=HEADERS,
        )
        soup = bs(r.text, "lxml")
        rows = soup.select(".row")[1:]
        result = []
        for row in rows:
            time = int(row.select(".time_24h")[0].text)
            if time == 24:
                time = 0
            time = datetime.time()
            symb = (
                list(row.select(".symb")[0].children)[0]["src"]
                .split("/")[-1]
                .replace(".svg", "")
            )
            temp = int(row.select(".temp_c")[0].text)
            feels_like = int(row.select(".temp_c")[1].text)
            hum = int(row.select(".humidity")[0].text[:-1])
            rain = float(row.select(".rain_mm")[0].text.replace(" mm", ""))
            wind_dir = list(row.select(".wind")[0].children)[0]["alt"]
            wind_speed = int(row.select(".wind_ms")[0].text)
            weather = HourForecast(
                time, temp, feels_like, symb, hum, wind_speed, wind_dir, rain
            )
            result.append(weather)
        return result

    def get_current(self) -> CurrentWeather:
        r = requests.get(
            self.CURRENT_URL.format(self._place.id, self._place.address),
            headers=HEADERS,
        )
        soup = bs(r.text, "lxml")
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
            datetime.datetime.now(),
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

    def get_forecast(self) -> List[DayForecast]:
        r = requests.get(self.FORECAST_URL.format(self._place.id), headers=HEADERS)
        result = r.json()[self._place.id]
        days = []
        for day in result:
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
            )
            days.append(day)
        return days

    def search_place(self, city_query) -> List[Place]:
        r = requests.get(
            self.SEARCH_URL.format(quote_plus(city_query)),
            params={"limit": 30, "lang": "ru"},
            headers=HEADERS,
        )
        if r.status_code == 200:
            result = r.json()
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
