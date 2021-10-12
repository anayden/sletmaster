from datetime import datetime
from typing import Generic, List, TypeVar, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

T = TypeVar("T")


class Area(Document):
    name: str
    owner: PydanticObjectId

    class Collection:
        name = "areas"


class ApplicableGroups(BaseModel):
    spo: bool = False
    sso: bool = False
    ssho: bool = False
    sop: bool = False
    smo: bool = False
    sservo: bool = False
    saoseo: bool = False
    sao: bool = False
    seo: bool = False
    all: bool = False

    @staticmethod
    def total() -> 'ApplicableGroups':
        return ApplicableGroups(spo=True, sso=True, ssho=True, sop=True, smo=True, sservo=True,
                                saoseo=True, sao=True, seo=True, all=True)


class Location(Document):
    name: str
    floor: Optional[int] = None
    parent: Optional[PydanticObjectId] = None

    class Collection:
        name = "locations"


class Person(Document):
    name: str
    brigade: Optional[str] = None
    manager: Optional[PydanticObjectId] = None
    phone: Optional[str] = None
    tg_id: Optional[str] = None
    vk_id: Optional[str] = None
    is_org: bool = False

    class Collection:
        name = "people"


class EventNews(Document):
    text: str
    created_at: datetime
    event: PydanticObjectId

    class Collection:
        name = "event_news"


class Event(Document):
    name: str
    start_time: datetime
    end_time: datetime
    status: Optional[str] = None
    status_time: Optional[datetime] = None
    parent: Optional[PydanticObjectId] = None
    can_be_parent: bool = False
    groups: ApplicableGroups
    owner: Optional[PydanticObjectId] = None
    location: Optional[PydanticObjectId] = None
    location_requirements: Optional[str] = None
    tech_requirements: Optional[str] = None
    public: Optional[bool] = True

    class Collection:
        name = "events"

    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp() * 1000),
        }


class Paged(Generic[T]):
    items: List[T]
    size: int
    more_pages: bool

    def __init__(self, number: int, items: List[T], more_pages: bool):
        self.items = items
        self.number = number
        self.more_pages = more_pages


__beanie_models__ = [Person, Location, Area, Event, EventNews]
