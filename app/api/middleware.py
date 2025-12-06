import time

from fastapi import Request, Response
from loguru import logger

from app.api.colors import colorize_code, colorize_method, colorize_time
from app.database.connection import DatabaseConnection


async def catch_errors(request: Request, call_next):
    with logger.catch(reraise=True):
        response = await call_next(request)
    return response


async def log(request: Request, call_next):
    time_start = time.perf_counter()
    response: Response = await call_next(request)
    time_end = time.perf_counter() - time_start
    logger.info(
        f"{colorize_time(time_end)} "
        f"{colorize_method(request.method)} "
        f"{colorize_code(response.status_code)} "
        f"{request.url.path} "
    )
    return response


async def acquire(request: Request, call_next):
    connection: DatabaseConnection = request.app.state.connection
    async with connection as conn:
        request.state.connection = conn
        return await call_next(request)
