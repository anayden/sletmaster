import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import List

import motor
from beanie import init_beanie
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect

from sletmaster.models import __beanie_models__, HatEvent
from sletmaster.settings import settings
from sletmaster.thehat.events.group_start import GroupStartEvent
from sletmaster.thehat.events.live_count import LiveCountEvent
from sletmaster.thehat.hat import Hat, groups

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            await new_event(LiveCountEvent(count=len(self.active_connections)), insert=False)
        except Exception as e:
            print(e)

    async def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except Exception as e:
            print(str(e))
        await new_event(LiveCountEvent(count=len(self.active_connections)), insert=False)

    async def broadcast(self, message: str):
        await asyncio.sleep(1)
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(str(e))


manager = ConnectionManager()


@app.on_event("startup")
async def startup_event():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection)
    await init_beanie(
        database=client[settings.mongo_db], document_models=__beanie_models__
    )


async def new_event(e: BaseModel, insert=True) -> None:
    e = HatEvent(created_at=datetime.now(), details=json.dumps(e.json()),
                 event_type=type(e).__name__)
    if insert:
        res = await HatEvent.insert_one(e)
        e.id = res.inserted_id
    else:
        e.id = uuid.uuid4()
    await manager.broadcast(str(e.json()))


@app.get("/start-hat")
async def get():
    for group_id, group_name in groups.items():
        if group_id > 4:
            continue
        hat = Hat(group_id, new_event)
        await new_event(GroupStartEvent(group_id=group_id, name=group_name))

        await hat.load()
        priority = 1
        res = await hat.iteration(priority)
        while res:
            priority += 1
            res = await hat.iteration(priority)
        await hat.random_dist()
    return None


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print(f"Client #{client_id} disconnected")
