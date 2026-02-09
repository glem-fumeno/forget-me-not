import asyncio
from datetime import datetime

import aiosqlite
from aiosqlite import Connection, Row, connect

from app.database.migrator import MigrationSequence


def adapt_datetime_epoch(val):
    return int(val.timestamp())


def convert_timestamp(val):
    return datetime.fromtimestamp(int(val))


aiosqlite.register_adapter(datetime, adapt_datetime_epoch)
aiosqlite.register_converter("timestamp", convert_timestamp)


class DatabaseConnection:
    def __init__(self, file: str) -> None:
        self.file = file
        self.connection: Connection | None

    async def connect(self):
        self.connection = await connect(self.file)
        await self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.row_factory = Row

    async def migrate(self):
        async with self as connection:
            await MigrationSequence(connection).run()

    async def close(self):
        if self.connection is None:
            return
        await asyncio.wait_for(self.connection.close(), 1)
        self.connection = None

    async def __aenter__(self) -> Connection:
        if self.connection is None:
            await self.connect()
            assert self.connection is not None, "Could not connect"
        return self.connection

    async def __aexit__(self, exc, val, tb):
        del val, tb
        assert self.connection is not None, "Connection dropped before exit"
        if exc is None:
            await self.connection.commit()
        else:
            await self.connection.rollback()
