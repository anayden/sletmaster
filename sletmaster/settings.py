from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_connection: Optional[str] = 'mongodb://spbso:08c1a9111d@mongo:27017/'
    mongo_db: Optional[str] = "sletmaster"


settings = Settings(_env_file=".env")
