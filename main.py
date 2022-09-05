import os
import uvicorn
from modules.texts import ES_FEEDBACK, ES_NOT_FOUND, ES_THANKS, ES_WELCOME, INITIAL_ROUTE, GATHER_ROUTE, get_sms_result
import wikipedia
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from modules.sms import send_bulk_sms
from fastapi import FastAPI, Form, Response
from dotenv import load_dotenv
load_dotenv()


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

    return Response(content=str(resp), media_type="application/xml")


@app.api_route(GATHER_ROUTE, methods=['GET', 'POST'])
def gather(From: str = Form(...), SpeechResult: str = Form(...)):
    resp = VoiceResponse()

    wikipedia.set_lang("es")

    try:
        res = wikipedia.summary(SpeechResult)
    except:
        resp.say(ES_NOT_FOUND)
        resp.redirect(INITIAL_ROUTE)

        return Response(content=str(resp), media_type="application/xml")

    send_bulk_sms(From, [
                  get_sms_result("es", res), ES_FEEDBACK])

    resp.say(res[:1000])
    resp.say(ES_THANKS)
    return Response(content=str(resp), media_type="application/xml")


if __name__ == "__main__":
    PORT = os.getenv("PORT", default=5000)
    # from pyngrok import ngrok
    # public_url = ngrok.connect(PORT, bind_tls=True).public_url
    # number = twilio_client.incoming_phone_numbers.list()[0]
    # number.update(voice_url=public_url + INITIAL_ROUTE)
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")
