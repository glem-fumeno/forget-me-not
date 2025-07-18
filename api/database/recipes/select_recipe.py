from api.database.operation import DatabaseOperation
from api.models.recipes.models import RecipeModel


class RecipeSelectRecipeOperation(DatabaseOperation):
    def run(self, user_id: int, recipe_id: int) -> RecipeModel | None:
        result = self.cursor.execute(self.query, (recipe_id, user_id))
        columns = result.fetchone()
        if columns is None:
            return
        return RecipeModel.from_db(result.description, columns)

    @property
    def query(self) -> str:
        return """
            SELECT recipe_id_, name_, icon_
            FROM recipes_
            INNER JOIN recipes_users_ USING (recipe_id_)
            WHERE recipe_id_ = ? AND user_id_ = ?
        """
