from dataclasses import dataclass

from app.services.domain.utils.enums import Direction


@dataclass
class Wind:
    speed: float
    direction: Direction
