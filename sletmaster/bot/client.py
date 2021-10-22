from aiohttp import ClientSession

from sletmaster.models import Event
from sletmaster.settings import settings


class BotClient:
    def __init__(self):
        self._session = ClientSession()

    async def check_event_status(self, event: Event) -> None:
        data = {
            "secret": '49092da65f25e8bcbefa9537a0cf5e6d266712d39c4144feda16cd67b5652949',
            "event_id": str(event.id),
            "event_name": event.name.strip(),
            "tg_user_id": int(event.tg_owner)
        }
        async with self._session.post(url=settings.bot_url, json=data) as resp:
            resp.raise_for_status()


bot_client = BotClient()
