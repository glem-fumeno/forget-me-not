import os
import sqlite3
from api.logging import logger


class Call:
    def __init__(self, cursor: sqlite3.Cursor):
        self.logger = logger
        self.cursor = cursor
        self.config = os.environ
