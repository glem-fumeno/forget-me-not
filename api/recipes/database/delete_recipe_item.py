from api.database.operation import DatabaseOperation


class RecipeDeleteRecipeItemOperation(DatabaseOperation):
    def run(self, recipe_id: int, item_id: int):
        self.cursor.execute(self.query, (recipe_id, item_id))

    @property
    def query(self) -> str:
        return """
            DELETE FROM recipes_items_ WHERE recipe_id_ = ? AND item_id_ = ?
        """
