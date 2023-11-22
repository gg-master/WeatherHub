from dataclasses import dataclass
import datetime
from typing import List
from app.services.domain.dto.location import Location
from app.services.domain.utils.enums import Direction


class WeatherConverter:
    _relevant_conditions_images = {
        "icon_thumb_bkn-p-ra-d" : "d320",
        "icon_thumb_bkn-p-ra-n" : "n320",
        "icon_thumb_bkn-p-sn-d" : "d322",
        "icon_thumb_bkn-p-sn-n" : "n322",
        "icon_thumb_bkn-m-ra-d" : "d210",
        "icon_thumb_bkn-m-ra-n" :  "n210",
        "icon_thumb_bkn-m-sn-d" : "d212",
        "icon_thumb_bkn-m-sn-n" : "n212",
        "icon_thumb_bkn-d" : "d200",
        "icon_thumb_bkn-n" : "n200",
        "icon_thumb_bkn-ra-d" : "d220",
        "icon_thumb_bkn-ra-n" : "n220",
        "icon_thumb_bkn-sn-d" : "d222",
        "icon_thumb_bkn-sn-n" : "n222",
        "icon_thumb_ovc" : "d400",
        "icon_thumb_ovc-p-ra" : "d430",
        "icon_thumb_ovc-p-sn" : "d432",
        "icon_thumb_ovc-m-ra" : "d410",
        "icon_thumb_ovc-m-sn" : "d412",
        "icon_thumb_ovc-ra" : "d420",
        "icon_thumb_ovc-ra-sn" : "d421",
        "icon_thumb_ovc-sn" : "d422",
        "icon_thumb_ovc-ts-ra" : "d440",
        "icon_thumb_skc-d" : "d000",
        "icon_thumb_skc-n" : "n000",
    }
    @staticmethod
    def wind_direction(wind_direction: str):
        winddir = None
        if wind_direction in ["С", "NORTH"]:
            winddir = Direction.N
        elif wind_direction in ["Ю", "SOUTH"]:
            winddir = Direction.S
        elif wind_direction in ["СВ", "NORTH_EAST"]:
            winddir = Direction.NE
        elif wind_direction in ["СЗ", "NORTH_WEST"]:
            winddir = Direction.NW
        elif wind_direction in ["ЮВ", "SOUTH_EAST"]:
            winddir = Direction.SE
        elif wind_direction in ["ЮЗ", "SOUTH_WEST"]:
            winddir = Direction.SW
        elif wind_direction in ["З", "WEST"]:
            winddir = Direction.W
        elif wind_direction in ["В", "EAST"]:
            winddir = Direction.E
        elif isinstance(wind_direction, int) or wind_direction.isdigit():
            winddir = Direction.from_degrees(int(wind_direction))
        return winddir

    @staticmethod
    def weather_condition(condition: str):
        condition = WeatherConverter._relevant_conditions_images[condition]

        condition = int(condition[1:])
        cloudness = condition // 100
        precip = condition // 10 % 10
        precip_type = condition % 10
        if cloudness > 4:
            cloudness -= 1
        return cloudness, precip, precip_type
    

@dataclass
class HourForecast:
    time: datetime.time
    temp: int
    condition: str
    feel_temp: int
    pressure: int
    wind_speed: int
    wind_direction: str
    wind_gust: float
    uv_index: int
    humidity: int
    visibility: int


@dataclass
class DayForecast:
    date: datetime.date
    temp: int
    feel_temp: int
    wind_speed: int
    wind_direction: int
    humidity: int
    condition: str
    sunrise: datetime.time
    sunset: datetime.time
    daylength: int # minutes
    hourly: List[HourForecast]


@dataclass
class CurrentWeather:
    datetime: datetime.datetime
    temp: int
    condition: str
    feel_temp: int
    humidity: int
    pressure: float
    wind_speed: int
    wind_direction: str
