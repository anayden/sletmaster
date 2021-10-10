from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter

from sletmaster.models import Location

locations_router = APIRouter()


@locations_router.get("/")
async def list() -> List[Location]:
    return await Location.all().to_list()


@locations_router.get("/{location_id}")
async def get(location_id: PydanticObjectId) -> Optional[Location]:
    location = await Location.get(location_id)
    return location


@locations_router.post("/")
async def create(location: Location) -> Location:
    result = await Location.insert_one(location)
    location.id = result.inserted_id
    return location


@locations_router.put("/{location_id}")
async def update(location_id: str, location: Location) -> Location:
    if str(location.id) != location_id:
        raise ValueError(f"location_id = {location_id}, location.id = {location.id}")
    await location.save()
    return location


@locations_router.delete("/{location_id}")
async def delete(location_id: PydanticObjectId) -> None:
    location = await Location.get(location_id)
    if location is not None:
        await location.delete()
    return None
