import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sletmaster.models import __beanie_models__
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


@app.get("/")
def index():
    return "OK"


@app.get("/seed")
async def seed():
    seed_people = True
    seed_areas = True
    seed_locations = True
    seed_events = True
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
    await init_beanie(
        database=client[settings.mongo_db], document_models=__beanie_models__
    )
    app.include_router(events_router, prefix="/events", tags=["events"])
    app.include_router(locations_router, prefix="/locations", tags=["locations"])
    app.include_router(people_router, prefix="/people", tags=["people"])
    app.include_router(areas_router, prefix="/areas", tags=["areas"])
