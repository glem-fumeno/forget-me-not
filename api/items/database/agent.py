import sqlite3

from api.core.agent import Agent
from api.items.database.delete import ItemDeleteCall
from api.items.database.insert import ItemInsertCall
from api.items.database.select import ItemSelectCall
from api.items.database.select_many import ItemSelectManyCall
from api.items.database.select_by_name import ItemSelectByNameCall
from api.items.database.update import ItemUpdateCall


class ItemAgent(Agent):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        super().__init__(cursor)
        cursor.execute(self.table_query)

        self.insert = self.wrap(ItemInsertCall)
        self.select = self.wrap(ItemSelectCall)
        self.select_many = self.wrap(ItemSelectManyCall)
        self.select_by_name = self.wrap(ItemSelectByNameCall)
        self.update = self.wrap(ItemUpdateCall)
        self.delete = self.wrap(ItemDeleteCall)

    @property
    def table_query(self):
        return """
        CREATE TABLE IF NOT EXISTS items_ (
            item_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            name_ TEXT NOT NULL,
            icon_ TEXT NOT NULL
        )
        """
