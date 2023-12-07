import asyncio
import datetime
import logging
from typing import List, Optional
from bs4 import BeautifulSoup as bs
import pytz

from app.services.infrastructure.weather_providers.yandex.dto import (
    CurrentWeather,
    DayForecast,
    HourForecast,
    Location,
)

from app.utils.requests import aiohttp_fetch, fetch_url, to_dict


class YandexPogodaProvider:
    _logger = logging.getLogger(__name__)

    CURRENT_URL = "https://yandex.ru/pogoda/?lat={}&lon={}"
    FORECAST_URL = (
        "https://yandex.ru/pogoda/ru-RU/details/day-{}?lat={}&lon={}"
    )

    @classmethod
    async def create_for(cls, location: Location) -> "YandexPogodaProvider":
        self = YandexPogodaProvider()
        self._location = location
        return self

    async def get_current(self) -> Optional[CurrentWeather]:
        self._location: Location
        path = self.CURRENT_URL.format(self._location.lat, self._location.long)
        headers = {
            "authority": "yandex.ru",
            "method": "GET",
            "path": path,
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Cookie": "mda=0; yandex_gid=38; yuidss=1137237821700071040; i=/vGYlsOU5NpapKXqV4ufZbMD/Qzgj+zWNc7GiINTdKqNgB31/P9dVqdL+HUVKGnU7E6TIYMvFzQpAJVhiYys219sRNk=; yandexuid=1137237821700071040; yashr=3652976771700071040; ymex=2015431041.yrts.1700071041; gdpr=0; _ym_uid=1700071041867503789; _ym_d=1700072111; spravka=dD0xNzAwMDcyMTUyO2k9MTI4Ljc1LjI0MC45MTtEPThDODJFNTVGMUNDNzY5MDkwNzlBRDU3QjMyMzQ4N0RENTk3RDlDQkY2N0Q5MTVGNDlGM0M5MzVBMzVDMTY1QzJGN0E5QzU0NzFERTI0RDM5NkZEMTlCNzRBMjlDQkM4RTdFMDBCQUFENEE5NUFERUJEQjlFMjYyNjM1Mjc0MDk1RjY1M0FCODJCNUE3QjNDNDQxNjREM0I0NjQxMjc2RTI1ODt1PTE3MDAwNzIxNTIyODI3Mzc3MjA7aD00YzE0Mjc3ZmJkY2E4Yzg2MTM4MjI5NzU0YTgwMTU5OA==; L=AwppYUJFVGBXVnFISHxGVVUIAX5uU2BbElY+RSZCNhwgNwBfXw==.1700072171.15527.352154.c044ac14f7df1d2675e19d94c4aef660; yandex_login=korshun.tolik; bltsr=1; skid=2993772881700169519; bh=EkEiR29vZ2xlIENocm9tZSI7dj0iMTE5IiwgIkNocm9taXVtIjt2PSIxMTkiLCAiTm90P0FfQnJhbmQiO3Y9IjI0IhoFIng4NiIiECIxMTkuMC42MDQ1LjE2MCIqAj8wMgIiIjoJIldpbmRvd3MiQggiMTAuMC4wIkoEIjY0IlJdIkdvb2dsZSBDaHJvbWUiO3Y9IjExOS4wLjYwNDUuMTYwIiwgIkNocm9taXVtIjt2PSIxMTkuMC42MDQ1LjE2MCIsICJOb3Q/QV9CcmFuZCI7dj0iMjQuMC4wLjAiWgI/MA==; KIykI=1; coockoos=3; device_id=a6cd582cd7f2cf6c51ef816aff894612bbda26a6d; active-browser-timestamp=1700255798003; ys=udn.cDprb3JzaHVuLnRvbGlr#wprid.1700345718476714-17302796251918021069-balancer-l7leveler-kubr-yp-sas-61-BAL-9872#c_chck.1738128295; font_loaded=YSv1; yp=1702663041.ygu.1#2015432171.udn.cDprb3JzaHVuLnRvbGlr#2015821587.pcs.1#1700851823.szm.1_25:1536x864:415x656#1702925423.hdrc.0#1731997588.p_sw.1700461587; Session_id=3:1700607066.5.0.1700072171784:W_BLgA:7.1.2:1|162033519.0.2.3:1700072171|3:10279025.103204.jQTF-7du-uHMe60UJ8tN-eN_Ohs; sessar=1.1184.CiDdscJGFzR2_rnA0BDB4pOFDsJZANDg5BYi1ks2yAd7Jw.84-CKxlctYCz1pk5Z044Tdw8VrngwSYwX5BaL4oM3bE; sessionid2=3:1700607066.5.0.1700072171784:W_BLgA:7.1.2:1|162033519.0.2.3:1700072171|3:10279025.103204.fakesign0000000000000000000; _ym_isad=1; is_gdpr=0; is_gdpr_b=CIrmCBC82wEoAg==; _yasc=1/CL+/YF5Ef0TZ2LKd1viMzDWDXbEWGSbJI03hGzmn6lk2yfZxy5dwO+Lts3EI7QsaZtGcJZSxNWR0BunsxxlrcQNw==; bh=Ej8iR29vZ2xlIENocm9tZSI7dj0iMTE5IiwiQ2hyb21pdW0iO3Y9IjExOSIsIk5vdD9BX0JyYW5kIjt2PSIyNCIaBSJ4ODYiIhAiMTE5LjAuNjA0NS4xNjAiKgI/MDoJIldpbmRvd3MiQggiMTAuMC4wIkoEIjY0IlJcIkdvb2dsZSBDaHJvbWUiO3Y9IjExOS4wLjYwNDUuMTYwIiwiQ2hyb21pdW0iO3Y9IjExOS4wLjYwNDUuMTYwIiwiTm90P0FfQnJhbmQiO3Y9IjI0LjAuMC4wIiI=; _ym_visorc=b",
            "Device-Memory": "8",
            "Downlink": "6.05",
            "Dpr": "1.25",
            "Ect": "4g",
            "Referer": "https://yandex.ru/pogoda/ru-RU/details?lat=48.707068&lon=44.516979&lang=ru&via=ms",
            "Rtt": "150",
            "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "Sec-Ch-Ua-Arch": "x86",
            "Sec-Ch-Ua-Bitness": "64",
            "Sec-Ch-Ua-Full-Version": "119.0.6045.160",
            "Sec-Ch-Ua-Full-Version-List": '"Google Chrome";v="119.0.6045.160", "Chromium";v="119.0.6045.160", "Not?A_Brand";v="24.0.0.0"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Model": "",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Ch-Ua-Platform-Version": "10.0.0",
            "Sec-Ch-Ua-Wow64": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Viewport-Width": "727",
        }
        status, text = await aiohttp_fetch(path)
        if status != 200:
            self._logger.warn(
                f"Couldn't get the current weather page. Resp status is: {status}"
            )
            return None
        try:
            soup = bs(text, "lxml")
            div_block = soup.find("div", class_="fact__temp-wrap")

            temp, feel_temp = map(
                lambda x: int(x.text.replace("−", "-")),
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
            wind_speed = int(
                float(
                    (
                        wind_block.find(
                            "span", class_="wind-speed"
                        ).text.replace(",", ".")
                    )
                )
            )
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
                datetime=datetime.datetime.now(tz=pytz.utc),
                temp=temp,
                condition=condition,
                feel_temp=feel_temp,
                humidity=hum,
                pressure=pressure,
                wind_speed=wind_speed,
                wind_direction=wind_dir,
            )

        except Exception as e:
            self._logger.error(f"Error parsing current weather. #> {e}")
            return None

    async def get_forecast(self) -> Optional[List[DayForecast]]:
        return await asyncio.gather(
            *[self._get_dayforecast(i) for i in range(10)]
        )

    async def _get_hourly(self, day: int) -> Optional[List[HourForecast]]:
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
        except Exception as e:
            self._logger.error(f"Error parsing hourly weather. #> {e}")
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

    async def _get_dayforecast(self, day: int) -> Optional[DayForecast]:
        status, text = await fetch_url(
            self.FORECAST_URL.format(
                day, self._location.lat, self._location.long
            )
        )
        if status != 200:
            self._logger.warn("Couldn't get the day forecast page")
            return None
        try:
            hours = await self._get_hourly(day)
            daypart = self._get_daypart_name(
                datetime.datetime.now(tz=self._location.timezone).time()
            )

            soup = bs(text, "lxml")
            raw_resp = to_dict(soup.find("script", id="__NEXT_DATA__").text)
            day_weather = raw_resp["props"]["pageProps"][
                "detailsMobileServerData"
            ]["weather"]["forecast"]["days"][day + 1]

            if day == 0:
                hours = hours[datetime.datetime.now(tz=self._location.timezone).time().hour:]

            return DayForecast(
                date=datetime.datetime.fromisoformat(day_weather["time"]),
                temp=day_weather["parts"][daypart]["temperature"],
                feel_temp=day_weather["parts"][daypart]["feelsLike"],
                wind_speed=day_weather["parts"][daypart]["windSpeed"],
                wind_direction=day_weather["parts"][daypart]["windDirection"],
                wind_gust=day_weather["parts"][daypart]["windGust"],
                pressure=day_weather["parts"][daypart]["pressure"],
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
        except Exception as e:
            self._logger.error(f"Error parsing day weather. #> {e}")
            return None
