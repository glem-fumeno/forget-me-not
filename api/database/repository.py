import sqlite3

from api.database.migrator import DatabaseMigrator

class DatabaseRepository:
    def __init__(self, database_path: str):
        self.database_path = database_path
        DatabaseMigrator().migrate(database_path)

    def __enter__(self):
        self.connect()
        return self

    def connect(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute('BEGIN')

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_val, exc_tb
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
