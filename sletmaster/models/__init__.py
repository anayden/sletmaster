from datetime import datetime
from enum import Enum
from typing import Generic, List, TypeVar, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, conint

T = TypeVar("T")


class Area(Document):
    name: str
    owner: PydanticObjectId

    class Collection:
        name = "areas"


class Vote(Document):
    event: PydanticObjectId
    crit_1: Optional[conint(ge=0, le=5)] = None
    crit_2: Optional[conint(ge=0, le=5)] = None
    crit_3: Optional[conint(ge=0, le=5)] = None
    created_at: datetime
    voted_at: datetime
    user: Optional[str] = None

    class Collection:
        name = "votes"


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
    brigades: Optional[List[str]] = None

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
    responsibilities: Optional[str] = None

    class Collection:
        name = "people"


class Participant(Document):
    name: str
    brigade: Optional[str] = None
    requests: Optional[List[PydanticObjectId]] = None
    any_event_in_groups: Optional[List[int]] = None
    registrations: Optional[List[PydanticObjectId]] = None

    class Collection:
        name = "participants"


class EventNews(Document):
    text: str
    created_at: datetime
    event: PydanticObjectId

    class Collection:
        name = "event_news"


class EventStatus(str, Enum):
    created = 'created'
    prep_issues = 'prep_issues'
    ready = 'ready'
    live_issues = 'live_issues'
    live_ok = 'live_ok'
    live_in_progress = 'live_in_progress'
    ended = 'ended'
    cancelled = 'cancelled'
    other = 'other'

    @property
    def needs_query(self) -> bool:
        return self in (EventStatus.ready, EventStatus.live_issues, EventStatus.live_ok,
                        EventStatus.live_in_progress)


class Event(Document):
    name: str
    start_time: datetime
    end_time: datetime
    status: Optional[EventStatus] = EventStatus.created
    status_time: Optional[datetime] = None
    parent: Optional[PydanticObjectId] = None
    can_be_parent: bool = False
    groups: ApplicableGroups
    owner: Optional[PydanticObjectId] = None
    tg_owner: Optional[str] = None
    last_tg_ping: Optional[datetime] = None
    location: Optional[PydanticObjectId] = None
    location_requirements: Optional[str] = None
    tech_requirements: Optional[str] = None
    public: Optional[bool] = True
    show_on_map: Optional[bool] = True
    competition: Optional[int] = None
    registration_group: Optional[int] = None
    min_participants: Optional[int] = None
    max_participants: Optional[int] = None

    class Collection:
        name = "events"

    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp() * 1000),
        }
        use_enum_values = True


class Paged(Generic[T]):
    items: List[T]
    size: int
    more_pages: bool

    def __init__(self, number: int, items: List[T], more_pages: bool):
        self.items = items
        self.number = number
        self.more_pages = more_pages


__beanie_models__ = [Person, Location, Area, Event, EventNews, Vote, Participant]
