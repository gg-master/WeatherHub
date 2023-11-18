
from typing import List
import urllib.parse
from app.services.domain.dto.location import Location

from app.utils.requests import fetch_url, to_dict


async def find_location(lang: str, query: str) -> List[Location]:
    encoded_part = urllib.parse.quote(query, encoding="utf-8")

    # api docs https://yandex.ru/dev/jsapi-v2-1/doc/ru/v2-1/ref/reference/geocode
    url = (
        f"https://suggest-maps.yandex.ru/suggest-geo?&lang={lang}&"
        f"search_type=weather_v2&client_id=weather_v2&part={encoded_part}"
    )

    status, text = await fetch_url(url)

    if status != 200:
        raise ConnectionError(status)

    allowed_kinds = ["locality"]
    filtered = list(
        filter(lambda x: x.get("kind") in allowed_kinds, to_dict(text)[1])
    )
    return list(map(lambda x: Location(x["name"], "", x["lat"], x["lon"]), filtered))

    