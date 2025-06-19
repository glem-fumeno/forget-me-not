import sqlite3


class DatabaseOperation:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor
