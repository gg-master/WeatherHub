import datetime

import pytz
from app.controllers.cache.cacher import PickleCacher
from app.controllers.views.dayblock import Block
from app.controllers.views.daycard import Card
from app.controllers.views.hourlycard import HourlyCard
from app.services.domain.dto.location import Location


class CachableList(list):
    _cached_timestamp: int


@PickleCacher(1)
def form_blocks(location: Location, current_weather, forecast):
    result = CachableList()
    now_date = datetime.datetime.now(location.timezone)
    card_list = map(lambda x: Card(x, location, x.provider), current_weather)
    result.append(
        Block(
            day_rel="Сейчас",
            date=now_date,
            city_in="в г. " + location.place,
            cards=list(enumerate(card_list)),
            location=location,
            is_time_viewed=True,
        )
    )
    day_count = 0
    for wforecast in forecast:
        day_count = max(len(wforecast.days), day_count)
    for day in range(day_count):
        day_cards = []
        date = now_date + datetime.timedelta(days=day)
        for wforecast in forecast:
            if day < len(wforecast.days):
                card = Card(wforecast.days[day], location, wforecast.provider)
                day_cards.append(card)

        if day == 0:
            day_rel = "Сегодня"
        elif day == 1:
            day_rel = "Завтра"
        else:
            day_rel = ""

        result.append(
            Block(
                day_rel=day_rel,
                date=date,
                city_in="в г. " + location.place,
                cards=list(enumerate(day_cards)),
                location=location,
                is_time_viewed=False,
            )
        )
    result._cached_timestamp = int(datetime.datetime.now().timestamp())
    return result


@PickleCacher(1)
def form_hourly_blocks(forecast, location):
    result = CachableList()
    now_date = datetime.datetime.now(location.timezone)
    day_count = 0
    for wforecast in forecast:
        day_count = max(len(wforecast.days), day_count)
    for day in range(day_count):
        day_cards = []
        date = now_date + datetime.timedelta(days=day)
        for wforecast in forecast:
            if day < len(wforecast.days):
                if wforecast.days[day].hourly is not None:
                    card = HourlyCard(
                        date,
                        wforecast.days[day].hourly,
                        location,
                        wforecast.provider,
                    )
                    day_cards.append(card)

        if day == 0:
            day_rel = "Сегодня"
        elif day == 1:
            day_rel = "Завтра"
        else:
            day_rel = ""

        if len(day_cards):
            result.append(
                Block(
                    day_rel=day_rel,
                    date=date,
                    city_in="в г. " + location.place,
                    cards=list(enumerate(day_cards)),
                    location=location,
                    is_time_viewed=False,
                )
            )
    result._cached_timestamp = int(datetime.datetime.now().timestamp())
    return result
