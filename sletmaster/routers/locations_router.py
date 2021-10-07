from typing import List

from fastapi import APIRouter

from sletmaster.models import Location

locations_router = APIRouter()


@locations_router.get("/")
async def list() -> List[Location]:
    return await Location.all().to_list()
