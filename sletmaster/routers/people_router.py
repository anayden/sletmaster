from typing import List

from fastapi import APIRouter

from sletmaster.models import Person

people_router = APIRouter()


@people_router.get("/")
async def list() -> List[Person]:
    return await Person.all().to_list()
