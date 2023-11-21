import asyncio
from flask import render_template, request, flash

from app.services.infrastructure.repositories import WeatherRepository
from app.views import form_blocks, form_hourly_blocks
from app.services.domain.dto.location import Location

from app.services.domain.get_current_forecast import GetCurrentForecast
from app.services.domain.get_tenday_forecast import GetTendayForecast
from app.services.search import find_location


TENDAY = GetTendayForecast(WeatherRepository())
CURRENT = GetCurrentForecast(WeatherRepository())


async def index():
    return render_template("index.html")


async def forecast():
    name = request.args.get("name")

    location = Location("Волгоград", "", 48.721322, 44.514226)
    if name:
        locations = await find_location("ru-RU", name)
        if len(locations):
            location = locations[0]
        else:
            flash(f"Ничего не найдено по запросу: {name}")
    current, tenday = await asyncio.gather(
        CURRENT.execute(location),
        TENDAY.execute(location),
    )
    blocks = form_blocks(location, current, tenday)
    return render_template("forecast.html", weather_forecast=blocks)


async def hourly():
    name = request.args.get("name")

    location = Location("Волгоград", "", 48.721322, 44.514226)
    if name:
        locations = await find_location("ru-RU", name)
        if len(locations):
            location = locations[0]
        else:
            flash(f"Ничего не найдено по запросу: {name}")
    hourly = await TENDAY.execute(location)
    blocks = form_hourly_blocks(location, hourly)
    return render_template("hourly.html", weather_forecast=blocks)
