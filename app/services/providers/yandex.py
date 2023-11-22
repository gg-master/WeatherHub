import requests
import urllib.parse
from pprint import pprint


city_name = "Москва"
encoded_city_name = urllib.parse.quote(city_name, encoding='utf-8')

url = f"https://suggest-maps.yandex.ru/suggest-geo?&lang=ru_RU&search_type=weather_v2&client_id=weather_v2&part={encoded_city_name}"

# Отправляем GET-запрос
response = requests.get(url)

# Проверяем, успешно ли выполнен запрос
if response.status_code == 200:
    # Выводим содержимое ответа
    pprint(response.text)
else:
    pprint(f"Запрос завершился с ошибкой: {response.status_code}")
