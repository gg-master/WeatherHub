import datetime
from app.controllers.views.dayblock import Block
from app.controllers.views.daycard import Card
from app.controllers.views.hourlycard import HourlyCard


def form_blocks(current_weather, forecast, location):
    result = []
    now_date = datetime.datetime.now()
    card_list = map(lambda x: Card(x, location, x.provider), current_weather)
    result.append(
        Block(day_rel="Сейчас", 
              date=now_date,
              city_in="в г. " + location.place,
              cards=list(enumerate(card_list)),
              location=location)
    )
    day_count = 0
    for wforecast in forecast:
        day_count = max(len(wforecast.days), day_count)
    for day in range(day_count):
        day_cards = []
        date = now_date.date() + datetime.timedelta(days=day)
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

        result.append(Block(
            day_rel=day_rel,
            date=date,
            city_in="в г. " + location.place,
            cards=list(enumerate(day_cards)),
            location=location)
        )
    return result


def form_hourly_blocks(forecast, location):
    result = []
    now_date = datetime.datetime.now()
    day_count = 0
    for wforecast in forecast:
        day_count = max(len(wforecast.days), day_count)
    for day in range(day_count):
        day_cards = []
        date = now_date.date() + datetime.timedelta(days=day)
        for wforecast in forecast:
            if day < len(wforecast.days):
                card = HourlyCard(wforecast.days[day].hourly, location, wforecast.provider)
                day_cards.append(card)

        if day == 0:
            day_rel = "Сегодня"
        elif day == 1:
            day_rel = "Завтра"
        else:
            day_rel = ""

        result.append(Block(
            day_rel=day_rel,
            date=date,
            city_in="в г. " + location.place,
            cards=list(enumerate(day_cards)),
            location=location)
        )
    return result
