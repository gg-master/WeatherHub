from dataclasses import dataclass
import datetime
from typing import List, Tuple, Union

from app.views.hourlycard import HourlyCard
from app.views.daycard import Card
from app.services.domain.dto.location import Location


@dataclass
class Block:
    day_rel: str
    date: datetime.datetime
    city_in: str
    cards: List[Tuple[int, Union[Card | HourlyCard]]]
    location: Location
    is_time_viewed: bool
