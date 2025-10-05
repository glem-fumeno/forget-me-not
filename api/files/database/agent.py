import sqlite3

from api.core.agent import Agent
from api.files.database.delete import FileDeleteCall
from api.files.database.insert import FileInsertCall
from api.files.database.select import FileSelectCall
from api.files.database.select_many import FileSelectManyCall
from api.files.database.select_by_name import FileSelectByNameCall
from api.files.database.update import FileUpdateCall


class FileAgent(Agent):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        super().__init__(cursor)
        cursor.execute(self.table_query)

        self.insert = self.wrap(FileInsertCall)
        self.select = self.wrap(FileSelectCall)
        self.select_many = self.wrap(FileSelectManyCall)
        self.select_by_name = self.wrap(FileSelectByNameCall)
        self.update = self.wrap(FileUpdateCall)
        self.delete = self.wrap(FileDeleteCall)

    @property
    def table_query(self):
        return """
        CREATE TABLE IF NOT EXISTS files_ (
            file_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            name_ TEXT NOT NULL,
            url_ TEXT
        )
        """
