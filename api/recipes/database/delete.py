from api.core.call import Call


class RecipeDeleteCall(Call):
    def run(self, recipe_id: int):
        self.cursor.execute(self.query, (recipe_id,))

    @property
    def query(self) -> str:
        return """
            DELETE FROM recipes_ WHERE recipe_id_ = ?
        """
