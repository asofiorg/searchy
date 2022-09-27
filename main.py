import os
import uvicorn
from modules.texts import ES_TRANSLATE_RESULT, ES_NEWS_HEADLINE, ES_FEEDBACK, ES_TRANSLATE, ES_NOT_FOUND, ES_THANKS, ES_WELCOME, INITIAL_ROUTE, START_ROUTE, TRANSLATE_ROUTE, get_sms_result
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from modules.sms import send_bulk_sms, send_sms
from modules.db import db, start_call, add_log
from fastapi import FastAPI, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules.wiki import search_wiki
from modules.classifier import classify
from modules.translate import translate
from modules.news import get_news
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
twilio_client = Client()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.api_route(INITIAL_ROUTE, methods=['GET', 'POST'])
def voice(From: str = Form(...), CallSid: str = Form(...)):
    start_call(CallSid, From)
    add_log(CallSid, "Searchy", ES_WELCOME)

    resp = VoiceResponse()

    gather = Gather(input="speech", language="es-US",
                    speech_timeout=5, action=START_ROUTE)
    gather.say(ES_WELCOME)
    resp.append(gather)

    resp.redirect(INITIAL_ROUTE)

    return Response(content=str(resp), media_type="application/xml")


@app.api_route(START_ROUTE, methods=['GET', 'POST'])
def start(From: str = Form(...), SpeechResult: str = Form(...), CallSid: str = Form(...)):
    add_log(CallSid, From, SpeechResult)

    resp = VoiceResponse()

    classify_result = classify(SpeechResult)

    if classify_result == "traducción":
        gather = Gather(input="speech", language="es-US",
                        speech_timeout=5, action=TRANSLATE_ROUTE)

        add_log(CallSid, "Searchy", ES_TRANSLATE)

        gather.say(ES_TRANSLATE)
        resp.append(gather)

        resp.redirect(INITIAL_ROUTE)

        return Response(content=str(resp), media_type="application/xml")

    if classify_result == "noticias":
        news = ES_NEWS_HEADLINE + " "

        news_data = get_news()

        for i in news_data:
            news += f"{i['title']}. "

        resp.say(news)
        add_log(CallSid, "Searchy", news)
        send_sms(From, news)

    if classify_result == "búsqueda":
        try:
            res = search_wiki(SpeechResult)
        except:
            resp.say(ES_NOT_FOUND)
            add_log(CallSid, "Searchy", ES_NOT_FOUND)

            return Response(content=str(resp), media_type="application/xml")

        resp.say(res[:1000])
        add_log(CallSid, "Searchy", res[:1000])
        send_sms(From, get_sms_result(res[:1000]))

    resp.say(ES_THANKS)
    add_log(CallSid, "Searchy", ES_THANKS)

    send_sms(From, ES_FEEDBACK)

    return Response(content=str(resp), media_type="application/xml")


@app.api_route(TRANSLATE_ROUTE, methods=['GET', 'POST'])
def start(From: str = Form(...), SpeechResult: str = Form(...), CallSid: str = Form(...)):
    add_log(CallSid, From, SpeechResult)

    resp = VoiceResponse()

    res = translate(SpeechResult)

    resp.say(ES_TRANSLATE_RESULT)
    resp.say(res, voice="Polly.Ivy", language="en")
    add_log(CallSid, "Searchy", f"{ES_TRANSLATE_RESULT} {res}")

    send_bulk_sms(From, [f"{ES_TRANSLATE_RESULT} {res}", ES_FEEDBACK])

    resp.say(ES_THANKS)
    add_log(CallSid, "Searchy", ES_THANKS)

    return Response(content=str(resp), media_type="application/xml")


if __name__ == "__main__":
    PORT = os.getenv("PORT", default=5000)
    # from pyngrok import ngrok
    # public_url = ngrok.connect(PORT, bind_tls=True).public_url
    # number = twilio_client.incoming_phone_numbers.list()[0]
    # number.update(voice_url=public_url + INITIAL_ROUTE)
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")
