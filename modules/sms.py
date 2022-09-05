from twilio.rest import Client

twilio_client = Client()


def send_sms(to, body):
    twilio_client.messages.create(
        body=body,
        to=to,
        from_=twilio_client.incoming_phone_numbers.list()[0].phone_number
    )

def send_bulk_sms(to, messages):
    for i in messages:
        send_sms(to, i)