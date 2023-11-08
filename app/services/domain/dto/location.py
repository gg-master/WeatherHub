from dataclasses import dataclass


@dataclass
class Location:
    place: str
    country: str
    lat: float
    long: float

    def __str__(self):
        return f"Location[place={self.place};country={self.country}]"
