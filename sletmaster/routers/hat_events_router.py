import logging
from typing import List

from fastapi import APIRouter

from sletmaster.models import HatEvent

hat_events_router = APIRouter()
logging.basicConfig()


@hat_events_router.get("/")
async def index() -> List[HatEvent]:
    return await HatEvent.all().to_list()
