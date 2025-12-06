from app.database.query import Query


class CreateItemTableMigration(Query):
    async def run(self):
        await self.connection.execute(self.query)

    @property
    def query(self) -> str:
        return """
            CREATE TABLE fmn_item_ (
                item_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
                name_ TEXT NOT NULL UNIQUE,
                icon_ TEXT,
                created_at_ TIMESTAMP,
                updated_at_ TIMESTAMP
            )
        """
