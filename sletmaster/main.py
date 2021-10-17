from secrets import compare_digest

import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from sletmaster.models import __beanie_models__
from sletmaster.routers.areas_router import areas_router
from sletmaster.routers.bot_router import bot_router
from sletmaster.routers.events_router import events_router
from sletmaster.routers.locations_router import locations_router
from sletmaster.routers.people_router import people_router
from sletmaster.routers.votes_router import votes_router
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
        if request.method != 'OPTIONS' and request.url.path != "/bot/check_events/99e7a75a477cfb0e67ec7d7862a5a4268a3edbf04e98937e5aa1ada3f7df881a":
            secret = request.headers.get("X-SPbSO-Secret", "")
            if not compare_digest(secret,
                                  "49092da65f25e8bcbefa9537a0cf5e6d266712d39c4144feda16cd67b5652949"):
                return Response(status_code=403, content="Unauthorized")
        response = await call_next(request)
        return response


app.add_middleware(CustomHeaderMiddleware)


@app.get("/")
async def index():
    return "OK"


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
    app.include_router(votes_router, prefix="/votes", tags=["votes"])
    app.include_router(bot_router, prefix="/bot", tags=["bot"])
