from beanie import PydanticObjectId
from datetime import datetime

from sletmaster.models import Location, Area, Person, Event, ApplicableGroups


def _sat(hour: int, minute: int) -> datetime:
    return datetime(2021, 10, 23, hour, minute)


def _sun(hour: int, minute: int) -> datetime:
    return datetime(2021, 10, 24, hour, minute)


async def create_events():
    seed_events = [
        Event(
            name="Заезд",
            start_time=_sat(9, 30),
            end_time=_sat(11, 00),
            groups=ApplicableGroups.total(),
            owner=PydanticObjectId("615f1a2b36361a0bf06b11ce")
        ),
        Event(
            name="Линейка открытия",
            start_time=_sat(11, 10),
            end_time=_sat(11, 30),
            groups=ApplicableGroups.total(),
            owner=PydanticObjectId("615f18094ae3eae87606a122"),
            location=PydanticObjectId("615f1a2b36361a0bf06b11d0")
        ),
        Event(
            name="Подготовка к ярмарке",
            start_time=_sat(11, 40),
            end_time=_sat(13, 00),
            groups=ApplicableGroups(spo=True),
            owner=PydanticObjectId("615f18094ae3eae87606a123")
        ),
        Event(
            name="Обед (1 волна)",
            start_time=_sat(13, 00),
            end_time=_sat(13, 30),
            groups=ApplicableGroups(spo=True),
            owner=PydanticObjectId("615f18094ae3eae87606a123"),
            location=PydanticObjectId("615f1a2b36361a0bf06b11ce")
        ),
        Event(
            name="Обед (2 волна)",
            start_time=_sat(14, 30),
            end_time=_sat(15, 00),
            groups=ApplicableGroups(sso=True, ssho=True, sop=True, smo=True, sservo=True,
                                    saoseo=True),
            owner=PydanticObjectId("615f18094ae3eae87606a123"),
            location=PydanticObjectId("615f1a2b36361a0bf06b11ce")
        ),
    ]
    await Event.insert_many(seed_events)


async def create_locations():
    base_seed_locations = [
        Location(name="Столовая"),  # 0
        Location(name="Ангар"),  # 1
        Location(name="Футбольное поле"),  # 2
        Location(name="1 учебный корпус"),  # 3
        Location(name="2 учебный корпус"),  # 4
        Location(name="1 жилой корпус"),  # 5
        Location(name="2 жилой корпус"),  # 6
    ]
    base_location_ids = (await Location.insert_many(base_seed_locations)).inserted_ids
    secondary_seed_locations = [
        Location(name="Комната 1", floor=1, parent=base_location_ids[3]),
        Location(name="Комната 2", floor=1, parent=base_location_ids[3]),
        Location(name="Комната 3", floor=1, parent=base_location_ids[3]),
        Location(name="Комната 1", floor=2, parent=base_location_ids[3]),
        Location(name="Комната 2", floor=2, parent=base_location_ids[3]),
        Location(name="Комната 3", floor=2, parent=base_location_ids[3]),
        Location(name="Комната 1", floor=1, parent=base_location_ids[4]),
        Location(name="Комната 2", floor=1, parent=base_location_ids[4]),
        Location(name="Комната 3", floor=1, parent=base_location_ids[4]),
        Location(name="Комната 1", floor=2, parent=base_location_ids[4]),
        Location(name="Комната 2", floor=2, parent=base_location_ids[4]),
        Location(name="Комната 3", floor=2, parent=base_location_ids[4]),
        Location(name="Левый холл", floor=1, parent=base_location_ids[5]),
        Location(name="Центральный холл", floor=1, parent=base_location_ids[5]),
        Location(name="Правый холл", floor=1, parent=base_location_ids[5]),
        Location(name="Левый холл", floor=2, parent=base_location_ids[5]),
        Location(name="Центральный холл", floor=2, parent=base_location_ids[5]),
        Location(name="Правый холл", floor=2, parent=base_location_ids[5]),
    ]
    await Location.insert_many(secondary_seed_locations)


async def create_areas():
    seed_areas = [
        Area(name="Дневная программа", owner=PydanticObjectId("615f18094ae3eae87606a122")),
        Area(name="Ночная программа", owner=PydanticObjectId("615f18094ae3eae87606a127")),
        Area(name="Быт и логистика", owner=PydanticObjectId("615f18094ae3eae87606a123")),
        Area(name="Конкурсы", owner=PydanticObjectId("615f18094ae3eae87606a125")),
    ]
    await Area.insert_many(seed_areas)


async def create_people():
    seed_people = [
        Person(name="Рита Шопен", is_org=True),
        Person(name="Диана Исламова", is_org=True),
        Person(name="Алексей Найден", is_org=True),
        Person(name="Лаврентьева Катя", is_org=True),
        Person(name="Кириленко Яна", is_org=True),
        Person(name="Угай Виталий", is_org=True),
    ]
    await Person.insert_many(seed_people)
