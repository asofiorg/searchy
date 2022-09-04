from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from modules.sms import send_bulk_sms
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import wikipedia
from modules.texts import ES_FEEDBACK, ES_NOT_FOUND, ES_THANKS, ES_WELCOME, INITIAL_ROUTE, GATHER_ROUTE, get_sms_result

app = FastAPI()
twilio_client = Client()


@app.api_route(INITIAL_ROUTE, methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()

    gather = Gather(input="speech", language="es-US",
                    speech_timeout=5, action=GATHER_ROUTE)
    gather.say(ES_WELCOME)
    resp.append(gather)

    resp.redirect(INITIAL_ROUTE)

    return str(resp)


@app.api_route(GATHER_ROUTE, methods=['GET', 'POST'])
def gather(request: Request):
    resp = VoiceResponse()

    text = request.values["SpeechResult"]

    wikipedia.set_lang("es")

    try:
        res = wikipedia.summary(text)
    except:
        resp.say(ES_NOT_FOUND)
        resp.redirect(INITIAL_ROUTE)

        return str(resp)

    send_bulk_sms(request.values["From"], [
                  get_sms_result("es", res), ES_FEEDBACK])

    resp.say(res[:1000])
    resp.say(ES_THANKS)
    return str(resp)
