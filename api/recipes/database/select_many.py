from api.core.call import Call
from api.recipes.models import RecipeModel


class RecipeSelectManyCall(Call):
    def run(self) -> dict[int, RecipeModel]:
        cursor = self.cursor.execute(self.query)
        results = cursor.fetchall()
        return {
            recipe_id: RecipeModel(recipe_id, name, icon)
            for (recipe_id, name, icon) in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT recipe_id_, name_, icon_ FROM recipes_
        """
