import dataclasses
import json
import urllib.parse

from flask import Response, abort, request
from app.services.search import find_location



async def location_search():
    lang = request.args.get("lang")
    query = request.args.get("query")

    print(query)
    try:
        result = await find_location(lang, query)
    except ConnectionError:
        return abort(500)
    
    result = list(map(lambda x: {"name": x.place, "lat": x.lat, "lon": x.long}, result))
    
    return Response(
        json.dumps({"query": query, "result": result}, ensure_ascii=False),
        200,
        mimetype="application/json",
    )
