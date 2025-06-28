from api.database.operation import DatabaseOperation
from api.recipes.schemas.models import RecipeModel


class RecipeUpdateRecipeOperation(DatabaseOperation):
    def run(self, model: RecipeModel):
        self.cursor.execute(self.query, (*model.parameters, model.recipe_id))

    @property
    def query(self) -> str:
        return """
            UPDATE recipes_
            SET
                name_ = ?,
                icon_ = ?
            WHERE
                recipe_id_ = ?
        """
