from typing import Optional

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    mongo_connection: Optional[str] = 'mongodb://root:example@localhost:27017/'
    mongo_db: Optional[str] = "demo_app_db"
    bot_url: Optional[HttpUrl] = "https://us-central1-spbso-295311.cloudfunctions.net/sletmaster_bot-check_status"


settings = Settings(_env_file=".env")
