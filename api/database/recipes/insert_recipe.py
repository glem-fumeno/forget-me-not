from api.database.operation import DatabaseOperation
from api.models.recipes.models import RecipeModel


class RecipeInsertRecipeOperation(DatabaseOperation):
    def run(self, user_id: int, model: RecipeModel):
        result = self.cursor.execute(self.query, model.parameters)
        assert result.lastrowid is not None, "could not insert recipe"
        model.recipe_id = result.lastrowid
        self.cursor.execute(self.user_query, (model.recipe_id, user_id))

    @property
    def query(self) -> str:
        return """
            INSERT INTO recipes_ (name_, icon_)
            VALUES (?, ?)
        """

    @property
    def user_query(self) -> str:
        return """
            INSERT INTO recipes_users_ (recipe_id_, user_id_)
            VALUES (?, ?)
        """
