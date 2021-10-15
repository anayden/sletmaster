from aiohttp import ClientSession

from sletmaster.models import Event
from sletmaster.settings import settings


class BotClient:
    def __init__(self):
        self._session = ClientSession()
        self._url = settings.bot_url

    async def check_event_status(self, event: Event) -> None:
        async with self._session.post(url=f"{self._url}/check_status/{event.tg_owner}",
                                      json={"event_name": event.name}) as resp:
            resp.raise_for_status()

bot_client = BotClient()