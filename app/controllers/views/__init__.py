import datetime
from app.controllers.views.dayblock import Block
from app.controllers.views.daycard import Card


def form_blocks(current_weather, forecast, location):
    result = []
    now_date = datetime.datetime.now()
    card_list = map(lambda x: Card(x, location, x.provider), current_weather)
    result.append(
        Block(day_rel="Сейчас", 
              date_info=now_date.date(), 
              time_info=now_date.time(),
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
            date_info=date,
            time_info="",
            city_in="в г. " + location.place,
            cards=list(enumerate(day_cards)),
            location=location)
        )
    return result


