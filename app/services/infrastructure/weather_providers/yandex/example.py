from dataclasses import dataclass
import datetime
from enum import Enum
from typing import Dict, Optional
from bs4 import BeautifulSoup
import requests
import urllib.parse
import json
from pprint import pprint

# from app.services.infrastructure.weather_providers.providers_contract import (
#     Location,
# )


def find_city(city_name: str, lang="ru_RU"):
    encoded_city_name = urllib.parse.quote(city_name, encoding='utf-8')
    url = f"https://suggest-maps.yandex.ru/suggest-geo?&lang=ru_RU&search_type=weather_v2&client_id=weather_v2&part={encoded_city_name}"

    response = requests.get(url)

    if response.status_code == 200:
        json_resp = response.json()
        json_formatted_str = json.dumps(
            json_resp, indent=2, ensure_ascii=False
        )
        # print(json_formatted_str)
        return json_resp[1][0]
    else:
        pprint(f"Запрос завершился с ошибкой: {response.status_code}")


# class Direction(Enum):
#     N = 1
#     S = 2
#     W = 3
#     E = 4
#     NW = 5
#     NE = 6
#     SW = 7
#     SE = 8


# @dataclass
# class Wind:
#     speed: float
#     direction: Direction


# @dataclass
# class Temperature:
#     real: float
#     feel: Optional[float]


# @dataclass
# class Weather:
#     temp: Temperature
#     wind: Wind
#     humidity: float
#     pressure: float
#     condition: str


# @dataclass
# class CurrentWeather(Weather):
#     provider: str
#     location: Location
#     date: datetime.datetime


# @dataclass
# class HourlyForecast(Weather):
#     time: datetime.time


# @dataclass
# class DayForecast(Weather):
#     min_temp: Temperature
#     hourly: Optional[HourlyForecast]


# @dataclass
# class WeatherForecast(Weather):
#     provider: str
#     location: Location
#     days: Dict[datetime.date, DayForecast]


# def get_weather_by_coordinates(latitude, longitude):
#     url = f"https://yandex.ru/pogoda/?lat={latitude}&lon={longitude}&via=srp"
#     response = requests.get(url)
#     if response.status_code == 200:
#         html = response.text

#         # Создаем объект BeautifulSoup
#         soup = BeautifulSoup(html, 'html.parser')

#         # Используем метод find() для поиска элемента с указанным классом и текстом
#         element = soup.find_all(
#             class_='title title_level_1 header-title__title'
#         )

#         # Проверяем, был ли элемент найден
#         if element:
#             print("Найден элемент:")
#             print(element)
#         else:
#             print("Элемент не найден")
#     else:
#         pprint(f"Запрос завершился с ошибкой: {response.status_code}")


# result = find_city('Волгоград')
# lat, lon = result['lat'], result['lon']
# get_weather_by_coordinates(lat, lon)

from requests import get
resp = get("https://yandex.ru/pogoda/?lat=51.66195309907495&lon=39.166753999409096")
print(resp.text)
