from pydantic import BaseModel


class LiveCountEvent(BaseModel):
    count: int
