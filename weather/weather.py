import requests
import datetime
from pprint import pprint

weather_token = '541acc03b121e060cf2a823215a83ea1'


def get_weather(city):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
        )
        data = r.json()
        if data["cod"] == '429' or data["cod"] == '404':
            raise Exception(data["message"])
        # pprint(data)

        cur_weather = data["main"]["temp"]
        max_weather = data["main"]["temp_max"]
        min_weather = data["main"]["temp_min"]
        weather_description = data["weather"][0]["main"]  # Облачность
        humidity = data["main"]["humidity"]  # Влажность
        wind = data["wind"]["speed"]  # Ветер

    except Exception as ex:
        print(ex)

    return {"temperature": cur_weather,
            "temperature_max": max_weather,
            "temperature min": min_weather,
            "weather_description": weather_description,
            "humidity": humidity,
            "wind": wind}


def main():
    print(get_weather("Moscow"))


if __name__ == '__main__':
    main()
