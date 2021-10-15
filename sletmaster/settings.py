from typing import Optional

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    mongo_connection: Optional[str] = 'mongodb://spbso:08c1a9111d@mongo:27017/'
    mongo_db: Optional[str] = "sletmaster"
    bot_url: Optional[HttpUrl] = "https://61694bf409e030001712c287.mockapi.io"


settings = Settings(_env_file=".env")
