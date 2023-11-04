from dataclasses import dataclass
from typing import List
from app.controllers.views.daycard import Card
from app.services.domain.dto.location import Location


@dataclass
class Block:
    day_rel: str
    date_info: str
    time_info: str
    city_in: str
    cards: List[Card]
    location: Location


