import random
from typing import List, Dict, Set, Optional

from sletmaster.models import Participant, Event
from sletmaster.thehat.events.get_best_small_event import GetBestSmallEventEvent
from sletmaster.thehat.events.iteration_end import IterationEndEvent
from sletmaster.thehat.events.iteration_start import IterationStartEvent
from sletmaster.thehat.events.random_dist import RandomDistEvent
from sletmaster.thehat.events.unused_people import UnusedPeopleEvent

groups = {
    1: 'Мастер-классы',
    2: 'Отрядные игры',
    3: 'Тренинги',
    4: 'Вечерняя программа ССО',
}


def matches_filter(brigade: str, group: int) -> bool:
    if 1 <= group <= 3:
        return brigade.startswith("СПО ") or brigade.startswith("МКСПО")
    if group == 4:
        return brigade.startswith("ССО ")
    raise ValueError(f"Unknown group {group}")


class Hat:
    def __init__(self, group_id: int, broadcast):
        self._group_id = group_id
        self._group_name = groups[group_id]
        self._events: Dict[str, Event] = {}
        self._participants: List[Participant] = []
        self._applicable_event_ids: Set[str] = set()
        self._registrations: Dict[str, List[Participant]] = {}
        self._broadcast = broadcast
        random.setstate(19481948)

    @property
    def registrations(self) -> Dict[str, List[Participant]]:
        return self._registrations

    async def load(self):
        parent_event = await Event.find_one(Event.registration_group == self._group_id)
        events_list = await Event.find(Event.parent == parent_event.id).to_list()
        self._events = {str(e.id): e for e in events_list}
        self._applicable_event_ids = {key for key in self._events.keys()}
        self._participants = await Participant.find_all().to_list()
        self._participants = [p for p in self._participants if
                              matches_filter(p.brigade, self._group_id)]
        self._participants = [p for p in self._participants if p.requests and len(
            p.requests) > 0 or p.any_event_in_groups and self._group_id in p.any_event_in_groups]
        for p in self._participants:
            p.requests = [req for req in p.requests if
                          str(req) in self._applicable_event_ids] if p.requests else []

    @staticmethod
    def _get_best_small_event_id(requests_by_event: Dict[str, List[Participant]]) -> Optional[str]:
        min_people = 999
        result = None
        for event_id, people in requests_by_event.items():
            if min_people > len(people):
                min_people = len(people)
                result = event_id
        return result

    def _get_best_large_event_id(self) -> Optional[str]:
        max_people = -1
        result = None
        for event in self._events.values():
            if event.max_participants > 0 and event.max_participants > max_people:
                max_people = event.max_participants
                result = str(event.id)
        return result

    async def _distribute(self, event: Event, requests: List[Participant]) -> List[Participant]:
        distribution: List[Participant] = []
        total_distributed_participants = 0
        while event.max_participants > 0 and len(requests) > 0:
            random_participant = requests.pop(random.randrange(len(requests)))
            distribution.append(random_participant)
            event.max_participants -= 1
        for r in distribution:
            total_distributed_participants += 1
            self._participants = [p for p in self._participants if p.id != r.id]
            lst = self._registrations.get(str(event.id), list())
            lst.append(r)
            self._registrations[str(event.id)] = lst
        return distribution

    async def random_dist(self) -> None:
        distribution: Dict[str, List[Participant]] = {}
        left = len(self._participants)  # people_left
        print(f'**** Starting random distribution of {left} people')
        total_places = 0  # places_left
        for e in self._events.values():
            total_places += e.max_participants
        print(f"**** I've got {total_places} places")
        total_distributed_participants = 0
        best_event_id = self._get_best_large_event_id()
        while best_event_id is not None and len(self._participants) > 0:
            best_event = self._events[best_event_id]
            distribution[str(best_event.id)] = await self._distribute(best_event,
                                                                      self._participants)
            selected_participants_cnt = len(distribution[str(best_event.id)])
            print(f'*** Added {selected_participants_cnt} to event {best_event.name}')
            total_distributed_participants += selected_participants_cnt
            best_event_id = self._get_best_large_event_id()
        print(f"*** Distributed {total_distributed_participants} randomly. "
              f"Left: {len(self._participants)}")
        rd_event = RandomDistEvent(group_id=self._group_id, people_left=left,
                                   places_left=total_places,
                                   distribution=distribution,
                                   events=[self._events[event_id] for event_id in
                                           distribution.keys()])
        await self._broadcast(rd_event)
        up_event = UnusedPeopleEvent(group_id=self._group_id, participants=self._participants)
        await self._broadcast(up_event)

    async def iteration(self, step: int) -> bool:
        if len(self._participants) == 0:
            print('==== No participants left')
            return False
        print(f'==== total participants at step {step}: {len(self._participants)}')

        requests_by_event: Dict[str, List[Participant]] = {}
        # build a map of current priorities
        total_requests = 0
        for p in self._participants:
            if len(p.requests) == 0:
                continue
            event_id = str(p.requests.pop(0))
            lst = requests_by_event.get(event_id, list())
            lst.append(p)
            requests_by_event[event_id] = lst
            total_requests += 1
        if total_requests == 0:
            print('==== No requests left')
            return False
        else:
            print(f'==== Have {total_requests} active requests at step {step}')
        it_start = IterationStartEvent(group_id=self._group_id, priority=step,
                                       total_requests=total_requests,
                                       events=[self._events[event_id] for event_id in
                                               requests_by_event.keys()],
                                       requests_by_event=requests_by_event)
        await self._broadcast(it_start)
        # list debug info
        for event_id, reqs in requests_by_event.items():
            event = self._events[event_id]
            print(f'{event.name}: {len(reqs)}/{event.max_participants}')
        # get event with minimal number of requests
        total_distributed_participants = 0
        best_event_id = self._get_best_small_event_id(requests_by_event)
        while best_event_id is not None:
            best_event = self._events[best_event_id]
            best_event_requests = requests_by_event.pop(best_event_id)
            print(f'Best event {best_event.name}: {len(best_event_requests)} '
                  f'for {best_event.max_participants} places')
            best_event_id = self._get_best_small_event_id(requests_by_event)

            best_event_requests_cnt = len(best_event_requests)
            places = best_event.max_participants
            distribution = await self._distribute(best_event, best_event_requests)

            best_small_event_event = GetBestSmallEventEvent(group_id=self._group_id,
                                                            event=best_event,
                                                            requests=best_event_requests_cnt,
                                                            places=places,
                                                            selected=distribution)
            await self._broadcast(best_small_event_event)

            total_distributed_participants += len(distribution)
            print(f'Selected participants: {[p.name for p in distribution]}')
            print(f'Leftover participants: {len(best_event_requests)}')
        print(f'==== Assigned {total_distributed_participants} out of {total_requests} requests')
        it_end = IterationEndEvent(group_id=self._group_id, priority=step,
                                   total_requests=total_requests,
                                   completed_requests=total_distributed_participants)
        await self._broadcast(it_end)
        return True

# async def main():
#     client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection)
#     await init_beanie(
#         database=client[settings.mongo_db], document_models=__beanie_models__
#     )
#
#
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
