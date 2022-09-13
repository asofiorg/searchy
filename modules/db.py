from deta import Deta
import os
from dotenv import load_dotenv
load_dotenv()


key = os.getenv("DATABASE_KEY")
db = Deta(key).Base("logs")


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
