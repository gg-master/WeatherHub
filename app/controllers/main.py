import asyncio
from flask import render_template, request

from app.services.infrastructure.repositories import WeatherRepository
from app.views import form_blocks, form_hourly_blocks
from app.services.domain.dto.location import Location

from app.services.domain.get_current_forecast import GetCurrentForecast
from app.services.domain.get_tenday_forecast import GetTendayForecast
from app.services.search import find_location


TENDAY = GetTendayForecast(WeatherRepository())
CURRENT = GetCurrentForecast(WeatherRepository())


async def index():
    name = request.args.get("name")

    if name:
        location = (await find_location("ru-RU", name))[0]
    else:
        location = Location("Волгоград", "", 48.721322, 44.514226)
    current, tenday = await asyncio.gather(
        CURRENT.execute(location),
        TENDAY.execute(location),
    )
    blocks = form_blocks(location, current, tenday)
    return render_template("index.html", weather_forecast=blocks)


async def hourly():
    name = request.args.get("name")

    if name:
        location = (await find_location("ru-RU", name))[0]
    else:
        location = Location("Волгоград", "", 48.721322, 44.514226)
    hourly = await TENDAY.execute(location)
    blocks = form_hourly_blocks(location, hourly)
    return render_template("hourly.html", weather_forecast=blocks)
