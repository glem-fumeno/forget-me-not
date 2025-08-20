from api.database.operation import DatabaseOperation
from api.models.recipes.models import RecipeModel


class RecipeInsertRecipeOperation(DatabaseOperation):
    def run(self, model: RecipeModel):
        result = self.cursor.execute(self.query, model.parameters)
        assert result.lastrowid is not None, "could not insert recipe"
        model.recipe_id = result.lastrowid

    @property
    def query(self) -> str:
        return """
            INSERT INTO recipes_ (name_, icon_)
            VALUES (?, ?)
        """
