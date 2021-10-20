from pydantic import BaseModel


class GroupStartEvent(BaseModel):
    group_id: int
    name: str
