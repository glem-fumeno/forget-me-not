from app.database.items.insert import ItemInsertQuery
from app.database.items.select import ItemSelectQuery
from app.database.items.select_by_name import ItemSelectByNameQuery
from app.database.base import QueriesBase
from app.database.connection import DatabaseConnection


class ItemQueries(QueriesBase):
    def __init__(self, connection: DatabaseConnection) -> None:
        self.connection = connection

        self.insert = self.wrap(ItemInsertQuery)
        self.select = self.wrap(ItemSelectQuery)
        self.select_by_name = self.wrap(ItemSelectByNameQuery)
