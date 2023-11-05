from dataclasses import dataclass
import datetime
from typing import List
from app.controllers.views.daycard import Card
from app.services.domain.dto.location import Location


@dataclass
class Block:
    day_rel: str
    date: datetime.datetime
    city_in: str
    cards: List[Card]
    location: Location


