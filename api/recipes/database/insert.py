from api.core.call import Call
from api.recipes.models import RecipeModel


class RecipeInsertCall(Call):
    def run(self, model: RecipeModel):
        cursor = self.cursor.execute(self.query, (model.name, model.icon))
        (recipe_id,) = cursor.fetchone()
        model.recipe_id = recipe_id

    @property
    def query(self) -> str:
        return """
            INSERT INTO recipes_ (name_, icon_) VALUES (?, ?) RETURNING recipe_id_
        """
