import requests


weather_token_ya = "3b23e8df-1028-45da-b96e-88afebfb84a9"


def fetch_current_temperature() -> dict[str, Exception] | int:
    try:
        r = requests.get(
            "https://api.weather.yandex.ru/v2/informers?lat=55.75396&lon=37.620393&[lang='ru_RU']",
            headers={"X-Yandex-API-Key": weather_token_ya},
        )
        data = r.json()
        temperature: int = data["fact"]["temp"]

    except Exception as ex:
        print(ex)
        return {"error": ex}

    return temperature
