from dataclasses import dataclass
from typing import Optional

@dataclass
class Temperature:
    real: float
    feel: Optional[float]
