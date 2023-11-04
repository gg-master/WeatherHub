from typing import Optional
import astral.sun
from astral import Observer
import datetime
from app.services.domain.dto.sun import SunPosition
from app.services.domain.dto.location import Location


class SunPositionService:
    def __init__(self, location: Location):
        self._loc = location
        self._observer = Observer(
            latitude=location.lat,
            longitude=location.long)
    
    def sunset(self, date: datetime.date) -> Optional[datetime.datetime]:
        result = astral.sun.sun(self._observer, date)
        return result.get("sunset")
    
    def sunrise(self, date: datetime.date) -> Optional[datetime.datetime]:
        result = astral.sun.sun(self._observer, date)
        return result.get("sunrise")
    
    def daylength(self, date: datetime.date) -> Optional[datetime.timedelta]:
        sunrise = self.sunrise(date)
        sunset = self.sunset(date)
        if sunrise and sunset:
            return sunset - sunrise
        
    def to_domain(self, date):
        return SunPosition(date, self.sunrise(date).time(),
                            self.sunset(date).time(), 
                            self.daylength(date).seconds // 60)