import json
import urllib.parse

from flask import Response, abort, jsonify, request

from app.utils.requests import fetch_url, to_dict


async def suggest_geo():
    lang = request.args.get("lang")
    part = request.args.get("part")

    encoded_part = urllib.parse.quote(part, encoding="utf-8")

    # api docs https://yandex.ru/dev/jsapi-v2-1/doc/ru/v2-1/ref/reference/geocode
    url = (
        f"https://suggest-maps.yandex.ru/suggest-geo?&lang={lang}&"
        f"search_type=weather_v2&client_id=weather_v2&part={encoded_part}"
    )

    status, text = await fetch_url(url)

    if status != 200:
        return abort(500)

    allowed_kinds = ["locality"]
    filtered = list(
        filter(lambda x: x.get("kind") in allowed_kinds, to_dict(text)[1])
    )
    return Response(
        json.dumps({"for": part, "options": filtered}),
        200,
        mimetype="application/json",
    )
