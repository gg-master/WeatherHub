from collections import namedtuple
import datetime
from app.services.domain.dto.weather import Weather as DomainWeather
from app.services.domain.utils.enums import Direction
from app.services.domain.utils.sun import SunPositionService

Temp = namedtuple("Temp", ["real", "feel"])
Wind = namedtuple("Temp", ["speed", "direction"])
Sun = namedtuple("Sun", ["sunset", "sunrise", "daylength"])

CLOUDNESS_INFO = {
    0: "Ясно",
    1: "Облачно с прояснениями",
    2: "Переменная облачность",
    3: "Облачно",
    4: "Пасмурно",
    5: "Туман",
}

RAIN_INFO = {
    1: "Небольшой дождь", 
    2: "Дождь", 
    3: "Ливень",
    4: "Гроза"
}

PRECIP_INFO = {1: "Дождь со снегом", 2: "Снег"}


class Card:
    def __init__(self, domain_weather, location, provider):
        if not isinstance(domain_weather, DomainWeather):
            raise TypeError("Invalid type, required domain weather")
        self._temp = domain_weather.temp
        self._wind = domain_weather.wind
        self._wind_gust = domain_weather.wind_gust
        self._humidity = domain_weather.humidity
        self._pressure = domain_weather.pressure
        self._condition = domain_weather.condition
        self._source = provider
        if hasattr(domain_weather, "sun"):
            self._sun = domain_weather.sun
        else:
            self._sun = SunPositionService(location).to_domain(datetime.datetime.now().date())

    def _translate_direction(self, direction):
        if direction == Direction.E:
            return "З"
        elif direction == Direction.W:
            return "В"
        elif direction == Direction.N:
            return "С"
        elif direction == Direction.S:
            return "Ю"
        elif direction == Direction.NE:
            return "СВ"
        elif direction == Direction.NW:
            return "СЗ"
        elif direction == Direction.SE:
            return "ЮВ"
        elif direction == Direction.SW:
            return "ЮЗ"
    
    @property
    def temp(self):
        return Temp(self._temp.real, self._temp.feel)
    
    @property
    def wind(self):
        return Wind(self._wind.speed, self._translate_direction(self._wind.direction))
    
    @property
    def wind_gust(self):
        if not self._wind_gust:
            return
        return Wind(self._wind_gust.speed, self._translate_direction(self._wind.direction))
    
    @property
    def humidity(self):
        return round(self._humidity, 3)
    
    @property
    def pressure(self):
        return self._pressure
    
    @property
    def condition_image(self):
        return f"img/sunwithcloud.png"
    
    @property
    def source(self):
        return self._source
    
    @property
    def condition(self):
        if self._condition.precipitation == 0:
            return CLOUDNESS_INFO[self._condition.cloudness]
        else:
            if self._condition.precipitation_type == 0:
                return RAIN_INFO[self._condition.precipitation]
            else:
                return PRECIP_INFO[self._condition.precipitation_type]

    @property
    def sun(self):
        return Sun(
            self._sun.sunset.strftime("%H:%M"),
            self._sun.sunrise.strftime("%H:%M"),
            "{}:{}".format(*divmod(self._sun.daylength, 60))
        )
    
