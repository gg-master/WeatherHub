from pprint import pprint
from flask import render_template
from app.services.domain.dto.location import Location

from app.services.domain.get_current_forecast import GetCurrentForecast
from app.services.domain.get_tenday_forecast import GetTendayForecast
from app.services.infrastructure.repositories import WeatherRepository


async def index():
    location = Location("Волгоград", "Россия", 48.721322, 44.514226)
    # pprint(await GetCurrentForecast(WeatherRepository()).execute(location))
    pprint(await GetTendayForecast(WeatherRepository()).execute(location))
    return render_template("index.html")
