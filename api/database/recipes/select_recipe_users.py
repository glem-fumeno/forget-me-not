from api.database.operation import DatabaseOperation


class RecipeSelectRecipeUsersOperation(DatabaseOperation):
    def run(self, recipe_id: int) -> set[int]:
        result = self.cursor.execute(self.query, (recipe_id,))
        results = result.fetchall()
        return {(columns[0]) for columns in results}

    @property
    def query(self) -> str:
        return """
            SELECT user_id_
            FROM recipes_users_
            WHERE recipe_id_ = ?
        """
