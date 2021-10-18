from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter

from sletmaster.models import Participant

participants_router = APIRouter()


@participants_router.get("/")
async def index() -> List[Participant]:
    return await Participant.all().to_list()


@participants_router.get("/{participant_id}")
async def get(participant_id: PydanticObjectId) -> Optional[Participant]:
    participant = await Participant.get(participant_id)
    return participant


@participants_router.post("/")
async def create(participant: Participant) -> Participant:
    result = await Participant.insert_one(participant)
    participant.id = result.inserted_id
    return participant


@participants_router.put("/{participant_id}")
async def update(participant_id: str, participant: Participant) -> Participant:
    if str(participant.id) != participant_id:
        raise ValueError(f"participant_id = {participant_id}, participant.id = {participant.id}")
    await participant.save()
    return participant


@participants_router.delete("/{participant_id}")
async def delete(participant_id: PydanticObjectId) -> None:
    participant = await Participant.get(participant_id)
    if participant is not None:
        await participant.delete()
    return None
