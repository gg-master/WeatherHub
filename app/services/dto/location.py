from dataclasses import dataclass

@dataclass
class Location:
    place: str
    country: str
    lat: float
    long: float