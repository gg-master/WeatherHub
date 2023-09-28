from dataclasses import dataclass
from app.services.enums import Direction

@dataclass
class Wind:
    speed: float
    direction: Direction