from api.database.operation import DatabaseOperation


class RecipeInsertRecipeUserOperation(DatabaseOperation):
    def run(self, recipe_id: int, user_id: int):
        self.cursor.execute(self.query, (recipe_id, user_id))

    @property
    def query(self) -> str:
        return """
            INSERT INTO recipes_users_ (recipe_id_, user_id_)
            VALUES (?, ?)
        """
