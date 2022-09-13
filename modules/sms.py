from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()


twilio_client = Client()


def send_sms(to, body):
    if to.startswith("+5757"):
        to = "+57" + to.split("+5757")[1]

    twilio_client.messages.create(
        body=body,
        to=to,
        from_=twilio_client.incoming_phone_numbers.list()[0].phone_number
    )


def send_bulk_sms(to, messages):
    for i in messages:
        send_sms(to, i)
