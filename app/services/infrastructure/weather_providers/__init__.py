from .foreca.provider import ForecaParser as ForecaProvider
from .foreca.mapper import Mapper as ForecaMapper
from .yandex.provider import YandexPogodaProvider
from .yandex.mapper import Mapper as YandexMapper
from .openweathermap.provider import OpenWeatherMapFetcher
from .openweathermap.mapper import Mapper as OpenWeatherMapMapper


registered_providers = {
    ForecaProvider: ForecaMapper,
    YandexPogodaProvider: YandexMapper,
    OpenWeatherMapFetcher: OpenWeatherMapMapper,
}