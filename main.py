import os
import uvicorn
from modules.texts import ES_TRANSLATE_RESULT, ES_NEWS_HEADLINE, ES_FEEDBACK, ES_TRANSLATE, ES_NOT_FOUND, ES_THANKS, ES_WELCOME, INITIAL_ROUTE, START_ROUTE, TRANSLATE_ROUTE, WEATHER_ROUTE, ES_WEATHER_PROMPT, ES_ASK_NEWSLETTER, NEWSLETTER_ROUTE, ADD_NEWSLETTER_ROUTE, FINAL_NEWSLETTER_ROUTE, ES_ASK_LOCATION, ES_DONE_NEWSLETTER, get_sms_result, get_weather_result
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from modules.sms import send_bulk_sms, send_sms
from modules.db import db, start_call, add_log, get_newsletter_subscribers, is_in_newsletter, add_newsletter
from fastapi import FastAPI, Form, Response, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from modules.wiki import search_wiki
from modules.classifier import classify
from modules.translate import translate
from modules.news import get_news
from modules.weather import get_weather
from modules.newsletter import get_newsletter_sms_list
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
twilio_client = Client()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def render_website(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request, "phone_number": "018005190663"})


@app.get(NEWSLETTER_ROUTE)
async def send_newsletter(password: str):
    if password == os.getenv("PASSWORD"):
        newsletter_messages = get_newsletter_sms_list()

        newsletter_subscribers = get_newsletter_subscribers()

        for i in newsletter_subscribers:
            if i["location"] != "False":
                sub_messages = newsletter_messages

                sub_messages.append(get_weather_result(
                    get_weather(i["location"])))

                send_bulk_sms(i["phone_number"], sub_messages)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"message": "Done"}


@app.api_route(INITIAL_ROUTE, methods=['GET', 'POST'])
def voice(From: str = Form(...), CallSid: str = Form(...)):
    start_call(CallSid, From)
    add_log(CallSid, "Searchy", ES_WELCOME)

    resp = VoiceResponse()

    gather = Gather(input="speech", language="es-US",
                    finish_on_key="#", action=START_ROUTE)
    gather.say(ES_WELCOME)
    resp.append(gather)

    resp.redirect(INITIAL_ROUTE)

    return Response(content=str(resp), media_type="application/xml")


@app.api_route(START_ROUTE, methods=['GET', 'POST'])
def start(From: str = Form(...), SpeechResult: str = Form(...), CallSid: str = Form(...)):
    add_log(CallSid, From, SpeechResult)

    resp = VoiceResponse()

    classify_result = classify(SpeechResult)

    if classify_result == "traducir a inglés" or classify_result == "traducir a español":
        locale = 'en' if classify_result == 'traducir a inglés' else 'es'

        gather = Gather(input="speech",
                        language="es-US" if locale == "en" else "en-US",
                        finish_on_key="#",
                        action=f"{TRANSLATE_ROUTE}?locale={locale}")

        add_log(CallSid, "Searchy", ES_TRANSLATE)

        gather.say(ES_TRANSLATE)
        resp.append(gather)

        resp.redirect(INITIAL_ROUTE)

        return Response(content=str(resp), media_type="application/xml")

    if classify_result == "clima":
        gather = Gather(input="speech", language="es-US",
                        finish_on_key="#", action=WEATHER_ROUTE)

        add_log(CallSid, "Searchy", ES_WEATHER_PROMPT)

        gather.say(ES_WEATHER_PROMPT)
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

        if is_in_newsletter(From):
            resp.say(ES_THANKS)
            add_log(CallSid, "Searchy", ES_THANKS)
            send_sms(From, ES_FEEDBACK)
        else:
            gather = Gather(input="dtmf", num_digits=1,
                            action=ADD_NEWSLETTER_ROUTE)
            gather.say(ES_ASK_NEWSLETTER)
            add_log(CallSid, "Searchy", ES_ASK_NEWSLETTER)
            resp.append(gather)

        return Response(content=str(resp), media_type="application/xml")

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

        if is_in_newsletter(From):
            resp.say(ES_THANKS)
            add_log(CallSid, "Searchy", ES_THANKS)
            send_sms(From, ES_FEEDBACK)
        else:
            gather = Gather(input="dtmf", num_digits=1,
                            action=ADD_NEWSLETTER_ROUTE)
            gather.say(ES_ASK_NEWSLETTER)
            add_log(CallSid, "Searchy", ES_ASK_NEWSLETTER)
            resp.append(gather)

        return Response(content=str(resp), media_type="application/xml")


@app.api_route(TRANSLATE_ROUTE, methods=['GET', 'POST'])
def translate_endpoint(From: str = Form(...), SpeechResult: str = Form(...), CallSid: str = Form(...), locale: str = "en"):
    add_log(CallSid, From, SpeechResult)

    resp = VoiceResponse()

    res = translate(SpeechResult, locale)

    resp.say(ES_TRANSLATE_RESULT)
    if locale == "en":
        resp.say(res, voice="Polly.Ivy", language="en")
    else:
        resp.say(res)

    add_log(CallSid, "Searchy", f"{ES_TRANSLATE_RESULT} {res}")

    send_sms(From, f"{ES_TRANSLATE_RESULT} {res}")

    if is_in_newsletter(From):
        resp.say(ES_THANKS)
        add_log(CallSid, "Searchy", ES_THANKS)
        send_sms(From, ES_FEEDBACK)
    else:
        gather = Gather(input="dtmf", num_digits=1,
                        action=ADD_NEWSLETTER_ROUTE)
        gather.say(ES_ASK_NEWSLETTER)
        add_log(CallSid, "Searchy", ES_ASK_NEWSLETTER)
        resp.append(gather)

    return Response(content=str(resp), media_type="application/xml")


@app.api_route(WEATHER_ROUTE, methods=['GET', 'POST'])
def weather_endpoint(From: str = Form(...), SpeechResult: str = Form(...), CallSid: str = Form(...)):
    add_log(CallSid, From, SpeechResult)

    resp = VoiceResponse()

    res = get_weather(SpeechResult)

    resp.say(get_weather_result(res))

    add_log(CallSid, "Searchy", get_weather_result(res))

    send_sms(From, get_weather_result(res))

    if is_in_newsletter(From):
        resp.say(ES_THANKS)
        add_log(CallSid, "Searchy", ES_THANKS)
        send_sms(From, ES_FEEDBACK)
    else:
        gather = Gather(input="dtmf", num_digits=1,
                        action=ADD_NEWSLETTER_ROUTE)
        gather.say(ES_ASK_NEWSLETTER)
        add_log(CallSid, "Searchy", ES_ASK_NEWSLETTER)
        resp.append(gather)

    return Response(content=str(resp), media_type="application/xml")


@app.api_route(ADD_NEWSLETTER_ROUTE, methods=['GET', 'POST'])
def newsletter_endpoint(From: str = Form(...), Digits: str = Form(...), CallSid: str = Form(...)):
    add_log(CallSid, From, Digits)

    resp = VoiceResponse()

    if Digits == "1":
        gather = Gather(input="speech", language="es-US",
                        finish_on_key="#", action=FINAL_NEWSLETTER_ROUTE)
        gather.say(ES_ASK_LOCATION)
        add_log(CallSid, "Searchy", ES_ASK_LOCATION)
        resp.append(gather)
    else:
        add_newsletter(From, "False")
        resp.say(ES_THANKS)
        add_log(CallSid, "Searchy", ES_THANKS)
        send_sms(From, ES_FEEDBACK)

    return Response(content=str(resp), media_type="application/xml")


@app.api_route(FINAL_NEWSLETTER_ROUTE, methods=['GET', 'POST'])
def final_newsletter_endpoint(From: str = Form(...), SpeechResult: str = Form(...), CallSid: str = Form(...)):
    add_log(CallSid, From, SpeechResult)

    resp = VoiceResponse()

    add_newsletter(From, SpeechResult)

    resp.say(ES_DONE_NEWSLETTER)
    add_log(CallSid, "Searchy", ES_DONE_NEWSLETTER)

    resp.say(ES_THANKS)
    add_log(CallSid, "Searchy", ES_THANKS)
    send_sms(From, ES_FEEDBACK)

    return Response(content=str(resp), media_type="application/xml")


if __name__ == "__main__":
    PORT = os.getenv("PORT", default=5000)
    from pyngrok import ngrok
    public_url = ngrok.connect(PORT, bind_tls=True).public_url
    number = twilio_client.incoming_phone_numbers.list()[1]
    number.update(voice_url=public_url + INITIAL_ROUTE)
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")
