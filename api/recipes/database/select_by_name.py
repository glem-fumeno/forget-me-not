from api.core.call import Call
from api.recipes.models import RecipeModel


class RecipeSelectByNameCall(Call):
    def run(self, name: str) -> RecipeModel | None:
        cursor = self.cursor.execute(self.query, (name,))
        result = cursor.fetchone()
        if result is None:
            return
        (recipe_id, icon) = result
        return RecipeModel(recipe_id, name, icon)

    @property
    def query(self) -> str:
        return """
            SELECT recipe_id_, icon_ FROM recipes_ WHERE name_ = ?
        """
