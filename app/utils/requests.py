import json
import httpx


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


async def fetch_url(url, headers={}, params={}):
    headers = dict(headers)
    headers.update(HEADERS)
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url=url, headers=headers, params=params, follow_redirects=True)
        return response.status_code, response.text


def to_dict(response):
    return json.loads(response)


def to_json(data):
    # TODO улучшить преобразование к json. Некоторые типы могут не приводиться.
    return json.dumps(data, ensure_ascii=False)
