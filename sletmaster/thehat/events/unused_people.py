from typing import List

from pydantic import BaseModel

from sletmaster.models import Participant


class UnusedPeopleEvent(BaseModel):
    group_id: int
    participants: List[Participant]
