from prisma import Prisma
from prisma.models import Call

db = Prisma()


async def start_call(call_sid, incoming_number):
    call = await db.call.create(
        data={
            "sid": call_sid,
            "incoming": incoming_number
        })

    return call


async def add_log(call_sid, sender, message):
    log = await db.log.create(
        data={
            "sender": sender,
            "message": message,
            call: {
                connectOrCreate: {
                    where: {
                        sid: call_sid
                    }
                }
            }
        })

    return log
