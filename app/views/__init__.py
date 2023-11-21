import datetime

from app.views.dayblock import Block
from app.views.daycard import Card
from app.views.hourlycard import HourlyCard
from app.services.domain.dto.location import Location


def form_blocks(location: Location, current_weather, forecast):
    result = []
    location_date = datetime.datetime.now(location.timezone)

    card_list = filter(
        lambda x: x is not None,
        map(
            lambda x: Card(
                x, location, x.provider,
                x.datetime.replace(tzinfo=datetime.timezone.utc)) if x is not None else None,
            current_weather,
        ),
    )
    result.append(
        Block(
            day_rel="Сейчас",
            date=location_date,
            city_in=location.place,
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
        date = location_date + datetime.timedelta(days=day)
        for wforecast in forecast:
            if wforecast is None:
                continue
            if day < len(wforecast.days):
                card = Card(
                    wforecast.days[day], location, wforecast.provider,
                    wforecast.datetime)
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
                city_in=location.place,
                cards=list(enumerate(day_cards)),
                location=location,
                is_time_viewed=False,
            )
        )
    return result


def form_hourly_blocks(location, forecast):
    result = []
    location_date = datetime.datetime.now(location.timezone)
    day_count = 0
    for wforecast in forecast:
        day_count = max(len(wforecast.days), day_count)
    for day in range(day_count):
        day_cards = []
        date = location_date + datetime.timedelta(days=day)
        for wforecast in forecast:
            if day < len(wforecast.days):
                if wforecast.days[day].hourly is not None:
                    card = HourlyCard(
                        date,
                        wforecast.datetime,
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
                    city_in=location.place,
                    cards=list(enumerate(day_cards)),
                    location=location,
                    is_time_viewed=False,
                )
            )
    return result
