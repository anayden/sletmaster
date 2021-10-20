from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter

from sletmaster.models import Vote, DbVote

votes_router = APIRouter()


@votes_router.get("/")
async def index() -> List[Vote]:
    return await Vote.all().to_list()


@votes_router.get("/{vote_id}")
async def get(vote_id: PydanticObjectId) -> Optional[DbVote]:
    vote = await DbVote.get(vote_id)
    return vote


@votes_router.post("/")
async def create(vote: Vote) -> DbVote:
    db_vote = DbVote(**vote.dict(), created_at=datetime.now())
    result = await Vote.insert_one(db_vote)
    db_vote.id = result.inserted_id
    return db_vote


@votes_router.put("/{vote_id}")
async def update(vote_id: PydanticObjectId, vote: Vote) -> Optional[DbVote]:
    if str(vote.id) != vote_id:
        raise ValueError(f"vote_id = {vote_id}, vote.id = {vote.id}")

    db_vote = await DbVote.get(vote_id)
    if db_vote is None:
        return None
    if db_vote.voted_at is not None:
        raise ValueError(f"vote_id = {vote_id} already saved")

    db_vote.voted_at = datetime.now()
    db_vote.crit_1 = vote.crit_1
    db_vote.crit_2 = vote.crit_2
    db_vote.crit_3 = vote.crit_3

    await db_vote.save()
    
    return db_vote

# @participants_router.delete("/{vote_id}")
# async def delete(vote_id: PydanticObjectId) -> None:
#     vote = await Vote.get(vote_id)
#     if vote is not None:
#         await vote.delete()
#     return None
