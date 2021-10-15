from typing import List

from fastapi import APIRouter

from sletmaster.models import Area

areas_router = APIRouter()


@areas_router.get("/")
async def index() -> List[Area]:
    return await Area.all().to_list()
