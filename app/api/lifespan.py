from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.config import get_config
from app.database.connection import DatabaseConnection


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    connection = DatabaseConnection(config.DB_FILE)
    with logger.catch(reraise=True):
        await connection.connect()
        await connection.migrate()
    app.state.connection = connection
    app.state.config = config
    logger.info(f"Started at {config.API_URL}")
    yield
    logger.info("Stopping...")
    await connection.close()
