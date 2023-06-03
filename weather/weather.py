from pprint import pprint

import datetime
import requests


# weather_token = '541acc03b121e060cf2a823215a83ea1'  # с сайта openweathermap.org
weather_token_ya = "3b23e8df-1028-45da-b96e-88afebfb84a9"


# с сайта openweathermap.org
# def get_weather(city):
#     try:
#         r = requests.get(
#             f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
#         )
#         data = r.json()
#         if data["cod"] != '200':
#             raise Exception(data["message"])
#         pprint(data)
#
#         cur_weather = data["main"]["temp"]
#         max_weather = data["main"]["temp_max"]
#         min_weather = data["main"]["temp_min"]
#         weather_description = data["weather"][0]["main"]  # Облачность
#         humidity = data["main"]["humidity"]  # Влажность
#         wind = data["wind"]["speed"]  # Ветер
#
#     except Exception as ex:
#         print(ex)
#
#     return {"temperature": cur_weather,
#             "temperature_max": max_weather,
#             "temperature min": min_weather,
#             "weather_description": weather_description,
#             "humidity": humidity,
#             "wind": wind}


def get_weather_Ya():
    # "GET https://api.weather.yandex.ru/v2/informers?
    #  lat=<широта>
    #  & lon=<долгота>
    #  & [lang=<язык ответа>]
    #
    # X-Yandex-API-Key: <значение ключа>"

    try:
        r = requests.get(
            f"https://api.weather.yandex.ru/v2/informers?lat=55.75396&lon=37.620393&[lang='ru_RU']",
            headers={"X-Yandex-API-Key": weather_token_ya},
        )
        data = r.json()
        # pprint(data)

    except Exception as ex:
        print(ex)

    return data


# def main():
#     print(get_weather_Ya())
#
#
# if __name__ == '__main__':
#     main()
