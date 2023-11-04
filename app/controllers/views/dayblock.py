from dataclasses import dataclass
from typing import List
from app.controllers.views.daycard import Card


@dataclass
class Block:
    day_rel: str
    date_info: str
    time_info: str
    city_in: str
    cards: List[Card]


