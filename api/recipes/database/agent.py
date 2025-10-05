import sqlite3

from api.core.agent import Agent
from api.recipes.database.delete import RecipeDeleteCall
from api.recipes.database.delete_item import RecipeDeleteItemCall
from api.recipes.database.insert import RecipeInsertCall
from api.recipes.database.insert_item import RecipeInsertItemCall
from api.recipes.database.select import RecipeSelectCall
from api.recipes.database.select_by_name import RecipeSelectByNameCall
from api.recipes.database.select_items import RecipeSelectItemsCall
from api.recipes.database.select_many import RecipeSelectManyCall
from api.recipes.database.update import RecipeUpdateCall


class RecipeAgent(Agent):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        super().__init__(cursor)
        cursor.execute(self.table_query)
        cursor.execute(self.join_query)

        self.insert = self.wrap(RecipeInsertCall)
        self.insert_item = self.wrap(RecipeInsertItemCall)
        self.select = self.wrap(RecipeSelectCall)
        self.select_items = self.wrap(RecipeSelectItemsCall)
        self.select_many = self.wrap(RecipeSelectManyCall)
        self.select_by_name = self.wrap(RecipeSelectByNameCall)
        self.update = self.wrap(RecipeUpdateCall)
        self.delete = self.wrap(RecipeDeleteCall)
        self.delete_item = self.wrap(RecipeDeleteItemCall)

    @property
    def table_query(self):
        return """
        CREATE TABLE IF NOT EXISTS recipes_ (
            recipe_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            name_ TEXT NOT NULL,
            icon_ TEXT NOT NULL
        )
        """

    @property
    def join_query(self):
        return """
        CREATE TABLE IF NOT EXISTS recipes_items_ (
            recipe_id_ INTEGER REFERENCES recipes_,
            item_id_ INTEGER REFERENCES items_
        )
        """
