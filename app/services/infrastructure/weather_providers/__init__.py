from .foreca.provider import ForecaParser as ForecaProvider
from .foreca.mapper import Mapper as ForecaMapper


registered_providers = {
    ForecaProvider: ForecaMapper
}