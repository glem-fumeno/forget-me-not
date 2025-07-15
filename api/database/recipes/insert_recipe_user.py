from api.database.operation import DatabaseOperation
from api.models.recipes.models import RecipeUserModel


class RecipeInsertRecipeUserOperation(DatabaseOperation):
    def run(self, model: RecipeUserModel):
        self.cursor.execute(self.query, model.parameters)

    @property
    def query(self) -> str:
        return """
            INSERT INTO recipes_users_ (recipe_id_, user_id_)
            VALUES (?, ?)
        """
