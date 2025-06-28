from api.database.operation import DatabaseOperation


class RecipeInsertRecipeItemOperation(DatabaseOperation):
    def run(self, recipe_id: int, item_id: int):
        self.cursor.execute(self.query, (recipe_id, item_id))

    @property
    def query(self) -> str:
        return """
            INSERT INTO recipes_items_ (recipe_id_, item_id_)
            VALUES (?, ?)
        """
