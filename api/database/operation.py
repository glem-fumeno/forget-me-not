import sqlite3

from loguru import logger

from api.context import Context


class DatabaseOperation:
    def __init__(self, ctx: Context, cursor: sqlite3.Cursor):
        self.cursor = cursor
        self.ctx = ctx
        self.logger = logger.bind(hash=self.ctx.get("hash", "00000000"))
        self.logger.debug(f"Operation: {self.__class__.__name__}")
