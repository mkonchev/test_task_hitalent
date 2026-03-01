import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5436"
    DB_NAME: str = "test_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1111"


settings = Settings()

IN_DOCKER = os.path.exists('/.dockerenv')


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
