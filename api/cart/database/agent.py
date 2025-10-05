import sqlite3

from api.cart.database.delete import CartDeleteCall
from api.cart.database.insert_many import CartInsertManyCall
from api.cart.database.select_many import CartSelectManyCall
from api.core.agent import Agent


class CartAgent(Agent):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        super().__init__(cursor)
        cursor.execute(self.table_query)

        self.insert_many = self.wrap(CartInsertManyCall)
        self.select_many = self.wrap(CartSelectManyCall)
        self.delete = self.wrap(CartDeleteCall)

    @property
    def table_query(self):
        return """
        CREATE TABLE IF NOT EXISTS cart_items_ (
            item_id_ INTEGER REFERENCES items_,
            origin_ TEXT
        )
        """
