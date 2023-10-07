import sys

sys.path.append("../../app")

from app.services.domain.dto.location import Location
import app.services.infrastructure.weather_providers.foreca.mapper as mapper

location = Location("Волгоград", "Россия", 48.721322, 44.514226)
current = mapper.get_current(location)
forecast = mapper.get_forecast(location)
positions = mapper.get_sun_position(location)
print(current)
print(forecast)
print(positions)
