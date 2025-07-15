from api.database.operation import DatabaseOperation
from api.models.recipes.models import RecipeModel


class RecipeSelectRecipesOperation(DatabaseOperation):
    def run(self, user_id: int) -> dict[int, RecipeModel]:
        result = self.cursor.execute(self.query, (user_id,))
        results = result.fetchall()
        return {
            columns[0]: RecipeModel.from_db(result.description, columns)
            for columns in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT recipe_id_, name_, icon_
            FROM recipes_
            INNER JOIN recipes_users_ USING (recipe_id_)
            WHERE user_id_ = ?
        """
