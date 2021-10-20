from typing import List, Dict

from pydantic import BaseModel

from sletmaster.models import Participant, Event


class RandomDistEvent(BaseModel):
    group_id: int
    people_left: int
    places_left: int
    events: List[Event]
    distribution: Dict[str, List[Participant]]
