# WeatherHub
Агрегатор погодных сервисов с возможностью просмотра 10-дневного и почасового прогноза погоды

**Требования к установке:** Python 3.8 и выше

## Установка и запуск

```
git clone https://github.com/gg-master/WeatherHub
cd WeatherHub
python -m pip install -r requirements.txt
python run.py
```

Для работы сервиса OpenWeatherMap требуется ключ. Создайте файл dev.env в папке проекта и укажите ключ в следующем формате:
```
OPENWEATHERMAP_KEY="ВАШ_КЛЮЧ"
```
