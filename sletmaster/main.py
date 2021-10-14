from secrets import compare_digest

import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from sletmaster.models import __beanie_models__, Location
from sletmaster.routers.areas_router import areas_router
from sletmaster.routers.events_router import events_router
from sletmaster.routers.locations_router import locations_router
from sletmaster.routers.people_router import people_router
from sletmaster.seeds import create_locations, create_areas, create_people, create_events
from sletmaster.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method != 'OPTIONS':
            secret = request.headers.get("X-SPbSO-Secret", "")
            if not compare_digest(secret,
                                  "49092da65f25e8bcbefa9537a0cf5e6d266712d39c4144feda16cd67b5652949"):
                return Response(status_code=403, content="Unauthorized")
        response = await call_next(request)
        return response


app.add_middleware(CustomHeaderMiddleware)


@app.get("/")
def index():
    return "OK"


@app.get("/seed_locations")
async def seed_locations_from_file():
    if False:
        lines = open('sletmaster/locations.txt').readlines()
        pparts = []
        for line in lines:
            parts = [p.strip() for p in line.strip().split(',')]
            if len(parts) == 3:
                parent = parts[0]
                floor = int(parts[1][0])
                name = parts[2]
                parent_loc = await Location.find_one(Location.name == parent)
                if not parent_loc:
                    parent_loc = await Location.insert_one((Location(name=parent)))
                parent_loc = await Location.find_one(Location.name == parent)
                await Location.insert_one(Location(name=name, floor=floor, parent=parent_loc.id))
            else:
                name = parts[0]
                await Location.insert_one(Location(name=name))
    return OK


@app.get("/seed")
async def seed():
    seed_people = False
    seed_areas = False
    seed_locations = False
    seed_events = False
    if seed_people:
        await create_people()
    if seed_areas:
        await create_areas()
    if seed_locations:
        await create_locations()
    if seed_events:
        await create_events()
    return "Seeded"


@app.on_event("startup")
async def startup_event():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection)
    print(settings.mongo_connection)
    await init_beanie(
        database=client[settings.mongo_db], document_models=__beanie_models__
    )
    app.include_router(events_router, prefix="/events", tags=["events"])
    app.include_router(locations_router, prefix="/locations", tags=["locations"])
    app.include_router(people_router, prefix="/people", tags=["people"])
    app.include_router(areas_router, prefix="/areas", tags=["areas"])
