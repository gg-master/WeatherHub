from dataclasses import dataclass
from typing import List
from app.services.domain.dto.location import Location
from app.services.domain.dto.weather import HourlyForecast


@dataclass
class HourlyCard:
    hourly: List[HourlyForecast]
    location: Location
    source: str