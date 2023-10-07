from dataclasses import dataclass
from typing import Optional


@dataclass
class Temperature:
    real: float  # Celsium
    feel: Optional[float]  # Celsium
