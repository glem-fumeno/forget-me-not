from api.core.call import Call
from api.recipes.models import RecipeModel


class RecipeSelectCall(Call):
    def run(self, recipe_id: int) -> RecipeModel | None:
        cursor = self.cursor.execute(self.query, (recipe_id,))
        result = cursor.fetchone()
        if result is None:
            return
        (name, icon) = result
        return RecipeModel(recipe_id, name, icon)

    @property
    def query(self) -> str:
        return """
            SELECT name_, icon_ FROM recipes_ WHERE recipe_id_ = ?
        """
