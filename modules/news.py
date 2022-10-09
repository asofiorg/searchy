import requests
import os
import datetime
from dotenv import load_dotenv
load_dotenv()


def get_news():
    today = datetime.datetime.now()

    API_KEY = os.getenv("NEWS_KEY")
    URL = f"http://api.mediastack.com/v1/news?access_key={API_KEY}&countries=co&date={today.year}-{today.month}-{today.day}"

    req = requests.get(URL)
    res = req.json()

    news = []

    for i in range(5):
        news.append({
            "title": res["data"][i]["title"],
            "description": res["data"][i]["description"]
        })

    return news
