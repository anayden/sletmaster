import datetime
import logging

from beanie import PydanticObjectId
from fastapi import APIRouter
from starlette.responses import Response

from sletmaster.bot.client import bot_client
from sletmaster.models import Event, EventStatus

bot_router = APIRouter()
logging.basicConfig()


@bot_router.put("/link/{event_id}/{tg_id}")
async def create_link(event_id: str, tg_id: str):
    event = await Event.get(PydanticObjectId(event_id))
    if event is None:
        return Response(status_code=404, content=f"Event {event_id} not found")
    event.tg_owner = tg_id
    await event.save()
    return Response(status_code=200, content=f"User {tg_id} is now owner of {event_id}")


@bot_router.put("/status/{event_id}/{status}")
async def status_response(event_id: str, status: EventStatus):
    event = await Event.get(PydanticObjectId(event_id))
    if event is None:
        return Response(status_code=404, content=f"Event {event_id} not found")
    event.status = status
    event.status_time = datetime.datetime.now()
    await event.save()
    return Response(status_code=200, content=f"OK")


@bot_router.get("/check_events/99e7a75a477cfb0e67ec7d7862a5a4268a3edbf04e98937e5aa1ada3f7df881a")
async def check_events():
    async for event in Event.find():
        if not event.status.needs_query:
            continue
        # TODO Check event start time
        bot_client.check_event_status(event)
