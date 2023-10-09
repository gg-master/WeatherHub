import sys
import time
import asyncio
import json
import dataclasses
import datetime

sys.path.append("../../")

from app.services.domain.utils.enums import Direction
from app.services.domain.dto.conditions import WeatherCondition
from app.services.domain.dto.location import Location
import app.services.infrastructure.weather_providers.foreca.mapper as mapper


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
    current = mapper.get_current(location)
    forecast = mapper.get_forecast(location)
    result = await asyncio.gather(current, forecast)
    end = time.monotonic()
    print("Time:", end - start)
    with open("weather.json", "w", encoding="utf-8") as fobj:
        json.dump(
            {"current": result[0], "forecast": result[1]},
            fobj,
            ensure_ascii=False,
            cls=EnhancedJSONEncoder,
            indent=4,
        )


asyncio.run(main())
