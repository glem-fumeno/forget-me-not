from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 55125
    API_URL: str = "http://0.0.0.0:55125"

    DB_FILE: str = "app.db"
    DB_TEST: str = "test.db"

    model_config = SettingsConfigDict(extra="allow")


@cache
def get_config():
    return Config()
