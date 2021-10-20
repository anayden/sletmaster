from typing import List, Dict

from pydantic import BaseModel

from sletmaster.models import Event, Participant


class IterationStartEvent(BaseModel):
    group_id: int
    priority: int
    total_requests: int
    events: List[Event]
    requests_by_event: Dict[str, List[Participant]]
