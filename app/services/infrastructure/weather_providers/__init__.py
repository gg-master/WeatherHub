from .foreca.provider import ForecaParser as ForecaProvider
from .foreca.mapper import Mapper as ForecaMapper
from .yandex.provider import YandexPogodaProvider
from .yandex.mapper import Mapper as YandexMapper


registered_providers = {
    ForecaProvider: ForecaMapper,
    YandexPogodaProvider: YandexMapper,
}