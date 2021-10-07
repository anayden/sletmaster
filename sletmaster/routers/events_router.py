from typing import List

from fastapi import APIRouter

from sletmaster.models import Event

events_router = APIRouter()


@events_router.get("/")
async def list() -> List[Event]:
    return await Event.all(sort="start_time").to_list()
