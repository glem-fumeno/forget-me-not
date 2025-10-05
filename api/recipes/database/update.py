from api.core.call import Call
from api.recipes.models import RecipeModel


class RecipeUpdateCall(Call):
    def run(self, model: RecipeModel):
        self.cursor.execute(
            self.query, (model.name, model.icon, model.recipe_id)
        )

    @property
    def query(self) -> str:
        return """
            UPDATE recipes_ SET name_ = ?, icon_ = ?
            WHERE recipe_id_ = ?
        """
