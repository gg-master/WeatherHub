from flask import render_template, request
from app.controllers.views import form_blocks, form_hourly_blocks
from app.services.domain.dto.location import Location

from app.services.domain.get_current_forecast import GetCurrentForecast
from app.services.domain.get_tenday_forecast import GetTendayForecast
from app.services.domain.get_hourly_forecast import GetHourlyForecast
from app.services.infrastructure.repositories import WeatherRepository
from app.services.search import find_location


async def index():
    name = request.args.get("name")

    if name:
        location = (await find_location("ru-RU", f"{name}"))[0]
    else:
        location = Location("Волгоград", "Россия", 48.721322, 44.514226)
    # TODO: change to asyncio.gather
    current = await GetCurrentForecast(WeatherRepository()).execute(location)
    tenday = await GetTendayForecast(WeatherRepository()).execute(location)
    blocks = form_blocks(location, current, tenday)
    return render_template("index.html", weather_forecast=blocks)


async def hourly():
    name = request.args.get("name")

    if name:
        location = (await find_location("ru-RU", f"{name}"))[0]
    else:
        location = Location("Волгоград", "Россия", 48.721322, 44.514226)
    hourly = await GetHourlyForecast(WeatherRepository()).execute(location)
    blocks = form_hourly_blocks(hourly, location)
    return render_template("hourly.html", weather_forecast=blocks)
