import asyncio
import sqlite3
import uuid
from typing import Any, Self

from api.cart.database.agent import CartAgent
from api.files.database.agent import FileAgent
from api.items.database.agent import ItemAgent
from api.recipes.database.agent import RecipeAgent

subscribers: dict[str, asyncio.Queue] = {}


class Agent:
    def __enter__(self) -> Self:
        self.connection = sqlite3.connect("app.db")
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        self.cursor.execute("BEGIN")

        self.items = ItemAgent(self.cursor)
        self.recipes = RecipeAgent(self.cursor)
        self.cart = CartAgent(self.cursor)
        self.files = FileAgent(self.cursor)
        return self

    async def notify(self, message: Any):
        to_unsubscribe = set()
        for id, subscriber in subscribers.items():
            if not subscriber.empty():
                to_unsubscribe.add(id)
            await subscriber.put(message)

        for id in to_unsubscribe:
            subscribers.pop(id)

    def subscribe(self, q: asyncio.Queue) -> str:
        id = uuid.uuid4().hex
        subscribers[id] = q
        return id

    def __exit__(self, exc_type, exc, tb) -> None:
        del exc_type, tb
        if exc is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
