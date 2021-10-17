from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter

from sletmaster.models import Vote

votes_router = APIRouter()


@votes_router.get("/")
async def index() -> List[Vote]:
    return await Vote.all().to_list()


@votes_router.get("/{vote_id}")
async def get(vote_id: PydanticObjectId) -> Optional[Vote]:
    vote = await Vote.get(vote_id)
    return vote


@votes_router.post("/")
async def create(vote: Vote) -> Vote:
    vote.created_at = datetime.now()
    result = await Vote.insert_one(vote)
    vote.id = result.inserted_id
    return vote

# @votes_router.put("/{vote_id}")
# async def update(vote_id: str, vote: Vote) -> Vote:
#     if str(vote.id) != vote_id:
#         raise ValueError(f"vote_id = {vote_id}, vote.id = {vote.id}")
#     await vote.save()
#     return vote


# @votes_router.delete("/{vote_id}")
# async def delete(vote_id: PydanticObjectId) -> None:
#     vote = await Vote.get(vote_id)
#     if vote is not None:
#         await vote.delete()
#     return None
