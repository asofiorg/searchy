import datetime
from modules.news import get_news


def get_newsletter_sms_list():
    today = datetime.datetime.now()

    news = get_news()

    sms = [f"Hola, este es el reporte para el {today.day} de {today.month} del {today.year} de parte de Searchy",
           "Las noticias para hoy:"]

    for i in news:
        sms.append(i["title"])

    return sms
