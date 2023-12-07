import os
import sys
import time
import asyncio
import json
import dataclasses
import datetime
from pathlib import Path

sys.path.insert(0, Path(__file__).parent.parent.parent.as_posix())

from app.services.domain.utils.enums import Direction
from app.services.domain.dto.conditions import WeatherCondition
from app.services.domain.dto.location import Location
from app.services.infrastructure.weather_providers.openweathermap.provider import OpenWeatherMapFetcher

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, WeatherCondition):
            return repr(o)
        elif isinstance(o, Direction):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, datetime.time):
            return o.strftime("%H:%M:%S")

        return super().default(o)


async def main():
    start = time.monotonic()
    location = Location("Волгоград", "Россия", 48.721322, 44.514226)
    provider = await OpenWeatherMapFetcher.create_for(location)
    current = provider.get_current()
    forecast = provider.get_forecast()
    current, forecast = await asyncio.gather(current, forecast)
    end = time.monotonic()
    print("Time:", end - start)
    with open("weather.json", "w", encoding="utf-8") as fobj:
        json.dump(
            {"current": current, "forecast": forecast},
            fobj,
            ensure_ascii=False,
            cls=EnhancedJSONEncoder,
            indent=4,
        )

asyncio.run(main())
