from api.database.operation import DatabaseOperation


class RecipeDeleteRecipeOperation(DatabaseOperation):
    def run(self, recipe_id: int):
        self.cursor.execute(self.query, (recipe_id,))

    @property
    def query(self) -> str:
        return """
            DELETE FROM recipes_ WHERE recipe_id_ = ?
        """
