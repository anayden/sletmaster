from typing import List, Dict

from pydantic import BaseModel

from sletmaster.models import Event, Participant


class IterationEndEvent(BaseModel):
    group_id: int
    priority: int
    total_requests: int
    completed_requests: int
