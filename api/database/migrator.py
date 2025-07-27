import os
import sqlite3

from loguru import logger

from api.singleton import Singleton


class DatabaseMigrator(metaclass=Singleton):
    def __init__(self):
        self.migrations_directory = "api/database/migrations"
        self.applied = False
        self.logger = logger

    def migrate(self, connection: sqlite3.Connection):
        if self.applied:
            return
        self.logger.debug("Migrating")
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.cursor.execute("BEGIN")
        self.logger.debug("Connected")
        try:
            self._ensure_migrations_table()
            applied_versions = self._get_applied_versions()
            files = sorted(os.listdir(self.migrations_directory))

            self.logger.debug(f"Found {files=}")
            for filename in files:
                version = filename.split("_")[0]
                if version in applied_versions:
                    continue
                path = os.path.join(self.migrations_directory, filename)
                with open(path, "r", encoding="utf-8") as f:
                    sql = f.read()
                self._apply_migration(version, sql)
                self.logger.debug(f"Applied migration {version}")
            self.connection.commit()
            self.applied = True
        except Exception as e:
            self.logger.critical(f"Exception occured: {e}")
            self.connection.rollback()

    def _ensure_migrations_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def _get_applied_versions(self):
        rows = self.cursor.execute(
            "SELECT version FROM schema_migrations"
        ).fetchall()
        return {row[0] for row in rows}

    def _apply_migration(self, version: str, sql: str):
        self.cursor.executescript(sql)
        self.cursor.execute(
            "INSERT INTO schema_migrations (version) VALUES (?)",
            (version,),
        )
