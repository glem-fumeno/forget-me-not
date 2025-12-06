from typing import Any

from aiosqlite import Connection, Row


class Query:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def fetchrow(self, *args: Any) -> Row | None:
        async with self.connection.execute(self.query, args) as cursor:
            return await cursor.fetchone()

    async def fetchval(self, *args: Any) -> Any | None:
        async with self.connection.execute(self.query, args) as cursor:
            result = await cursor.fetchone()
            return None if result is None else result[0]

    @property
    def query(self) -> str: ...
