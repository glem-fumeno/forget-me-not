from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.controllers.recipes.core import RecipeController
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.responses import RecipeResponse


class RecipeDeleteController(RecipeController):
    def run(self, recipe_id: int) -> RecipeResponse:
        self.validate_access()
        model = self.repository.select_recipe(self.issuer.user_id, recipe_id)
        if model is None:
            raise RecipeNotFoundError
        recipe_items = self.repository.select_recipe_items(recipe_id)
        self.repository.delete_recipe(recipe_id)
        return RecipeResponse.from_model(model, recipe_items)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /recipes/{recipe_id}",
            path={"recipe_id": "integer"},
            responses=RecipeResponse,
            errors=[LoggedOut, RecipeNotFoundError],
        )
