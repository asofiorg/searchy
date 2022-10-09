import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_weather(place):
    API_KEY = os.getenv("WEATHER_KEY")
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}&lang=es"

    req = requests.get(URL)
    res = req.json()

    weather = {
        "name": res["name"],
        "description": res["weather"][0]["description"],
        "temperature": round(res["main"]["temp"] - 273.15)
    }

    return weather
