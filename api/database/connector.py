import sqlite3

from api.context import Context
from api.database.migrator import DatabaseMigrator
from config import get_config


class DatabaseConnector:
    def __init__(self, ctx: Context, database_path: str | None = None):
        self.ctx = ctx
        self.config = get_config()
        self.database_path = self.config.DB_PATH
        self.migrator = DatabaseMigrator()
        if database_path is not None:
            self.database_path = database_path
            self.migrator.applied = False

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.migrator.migrate(self.connection)
        self.cursor = self.connection.cursor()
        self.cursor.execute("BEGIN")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_val, exc_tb
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
