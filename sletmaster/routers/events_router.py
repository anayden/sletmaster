from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter

from sletmaster.models import Event

events_router = APIRouter()


@events_router.get("/")
async def list() -> List[Event]:
    return await Event.all(sort="start_time").to_list()


@events_router.get("/{event_id}")
async def get(event_id: PydanticObjectId) -> Optional[Event]:
    event = await Event.get(event_id)
    return event


@events_router.post("/")
async def create(event: Event) -> Event:
    result = await Event.insert_one(event)
    event.id = result.inserted_id
    return event


@events_router.put("/{event_id}")
async def update(event_id: str, event: Event) -> Event:
    if str(event.id) != event_id:
        raise ValueError(f"event_id = {event_id}, event.id = {event.id}")
    await event.save()
    return event


@events_router.delete("/{event_id}")
async def delete(event_id: PydanticObjectId) -> None:
    event = await Event.get(event_id)
    if event is not None:
        await event.delete()
    return None
