from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 5000
    FRONTEND_URL: str = "http://localhost:8080"
    SALT: str = "e7c04613-2a6c-423e-987c-624d14de8a8e"
    DB_PATH: str = "app.db"
    LOG_FILE: str = ""
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8", env_file=".env"
    )


@lru_cache()
def get_config() -> Config:
    return Config()
