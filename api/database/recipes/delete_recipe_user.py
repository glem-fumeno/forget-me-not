from api.database.operation import DatabaseOperation


class RecipeDeleteRecipeUserOperation(DatabaseOperation):
    def run(self, recipe_id: int, user_id: int):
        self.cursor.execute(self.query, (recipe_id, user_id))

    @property
    def query(self) -> str:
        return """
            DELETE FROM recipes_users_ WHERE recipe_id_ = ? AND user_id_ = ?
        """
