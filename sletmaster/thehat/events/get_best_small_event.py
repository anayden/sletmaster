from typing import List, Dict

from pydantic import BaseModel

from sletmaster.models import Event, Participant


class GetBestSmallEventEvent(BaseModel):
    group_id: int
    event: Event
    requests: int
    places: int
    selected: List[Participant]
