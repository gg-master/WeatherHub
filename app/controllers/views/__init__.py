import datetime
from app.controllers.views.dayblock import Block
from app.controllers.views.daycard import Weather


def form_blocks(current_weather, forecast, location):
    result = []
    now_date = datetime.datetime.now()
    result.append(
        Block(day_rel="Сейчас", 
              date_info=now_date.date(), 
              time_info=now_date.time(),
              city_in="в г. " + location.place,
              cards=list(enumerate(map(lambda x: Weather(x, location), current_weather))))
    )
    day_count = 0
    for wforecast in forecast:
        day_count = max(len(wforecast.days), day_count)
    for day in range(day_count):
        day_cards = []
        date = now_date.date() + datetime.timedelta(days=day)
        for wforecast in forecast:
            if day < len(wforecast.days):
                day_cards.append(Weather(wforecast.days[day], location))

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
            cards=list(enumerate(day_cards)))
        )
    return result


