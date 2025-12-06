from fastapi import Depends, Request

from app.database.items.queries import ItemQueries
from app.database.connection import DatabaseConnection


class Queries:
    def __init__(self, connection: DatabaseConnection) -> None:
        self.items = ItemQueries(connection)


def get_db_queries(request: Request):
    return Queries(request.state.connection)


QueriesDepends = Depends(get_db_queries)
