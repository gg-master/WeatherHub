import sys
import time
import asyncio

sys.path.append("../../")

from app.services.domain.dto.location import Location
import app.services.infrastructure.weather_providers.foreca.mapper as mapper


async def main():
    start = time.monotonic()
    location = Location("Волгоград", "Россия", 48.721322, 44.514226)
    current = mapper.get_current(location)
    forecast = mapper.get_forecast(location)
    result = await asyncio.gather(current, forecast)
    end = time.monotonic()
    print("Time:", end - start)
    print(result)


asyncio.run(main())
