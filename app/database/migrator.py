from aiosqlite import Connection
from loguru import logger

from app.database.migrations.create_item_table import (
    CreateItemTableMigration,
)


def pascal_to_kebab(value: str) -> str:
    result = ""
    for ch in value:
        if ch.isupper():
            result += "-"
        result += ch.lower()
    return result.removeprefix("-")


class MigrationSequence:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.migrations = [
            CreateItemTableMigration(connection),
        ]

    async def run(self):
        await self.connection.execute(self.table_query)
        migrations = await self.connection.execute_fetchall(self.select_query)
        migrations = {migration["name_"] for migration in migrations}

        for migration in self.migrations:
            name = pascal_to_kebab(
                migration.__class__.__name__.removesuffix("Migration")
            )
            if name in migrations:
                continue
            await migration.run()
            await self.connection.execute(self.insert_query, (name,))
            logger.info(f"applied migration {name}")

    @property
    def table_query(self) -> str:
        return """
            CREATE TABLE IF NOT EXISTS migration_ (
                name_ TEXT PRIMARY KEY,
                executed_at_ TIMESTAMP NOT NULL DEFAULT current_timestamp
            )
        """

    @property
    def select_query(self) -> str:
        return """
            SELECT name_ FROM migration_
        """

    @property
    def insert_query(self) -> str:
        return """
            INSERT INTO migration_ (name_)
            VALUES (?)
        """
