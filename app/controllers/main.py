from collections import namedtuple
import datetime
import time
from flask import render_template
from numpy import append
from app.controllers.views import form_blocks
from app.services.domain.dto.location import Location

from app.services.domain.get_current_forecast import GetCurrentForecast
from app.services.domain.get_tenday_forecast import GetTendayForecast
from app.services.infrastructure.repositories import WeatherRepository



async def index():
    location = Location("Волгоград", "Россия", 48.721322, 44.514226)
    current = await GetCurrentForecast(WeatherRepository()).execute(location)
    tenday = await GetTendayForecast(WeatherRepository()).execute(location)
    blocks = form_blocks(current, tenday, location)
    return render_template("index.html", weather_forecast=blocks)
