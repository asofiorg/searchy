from deta import Deta
import os
from dotenv import load_dotenv
load_dotenv()


key = os.getenv("DATABASE_KEY")
db = Deta(key).Base("logs")
newsletter_db = Deta(key).Base("newsletter")


def start_call(call_sid, incoming_number):
    call = db.put({
        "incoming": incoming_number,
        "logs": []
    }, call_sid)

    return call


def add_log(call_sid, sender, message):
    call = db.get(call_sid)

    call["logs"].append({
        "sender": sender,
        "message": message
    })

    log = db.put(call, call_sid)

    return log


def add_newsletter(phone_number, location):
    return newsletter_db.put({"phone_number": phone_number, "location": location}, phone_number)


def is_in_newsletter(phone_number):
    return newsletter_db.fetch({"phone_number": phone_number})._count > 0


def get_newsletter_subscribers():
    return newsletter_db.fetch()._items
