from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter

from sletmaster.models import Person

people_router = APIRouter()


@people_router.get("/")
async def index() -> List[Person]:
    return await Person.all().to_list()


@people_router.get("/{person_id}")
async def get(person_id: PydanticObjectId) -> Optional[Person]:
    person = await Person.get(person_id)
    return person


@people_router.post("/")
async def create(person: Person) -> Person:
    result = await Person.insert_one(person)
    person.id = result.inserted_id
    return person


@people_router.put("/{person_id}")
async def update(person_id: str, person: Person) -> Person:
    if str(person.id) != person_id:
        raise ValueError(f"person_id = {person_id}, person.id = {person.id}")
    await person.save()
    return person


@people_router.delete("/{person_id}")
async def delete(person_id: PydanticObjectId) -> None:
    person = await Person.get(person_id)
    if person is not None:
        await person.delete()
    return None
