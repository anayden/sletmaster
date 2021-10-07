from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_connection: str
    mongo_db = "demo_app_db"

settings = Settings(_env_file=".env")