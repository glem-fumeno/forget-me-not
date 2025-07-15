from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.controllers.recipes.core import RecipeController
from api.models.recipes.errors import ItemNotFoundError, RecipeNotFoundError
from api.models.recipes.responses import RecipeResponse


class RecipeAddToRecipeController(RecipeController):
    def run(self, recipe_id: int, item_id: int) -> RecipeResponse:
        self.validate_access()
        model = self.repository.select_recipe(self.issuer.user_id, recipe_id)
        if model is None:
            raise RecipeNotFoundError
        items = self.repository.select_items()
        if item_id not in items:
            raise ItemNotFoundError

        self.repository.insert_recipe_item(recipe_id, item_id)
        return RecipeResponse.from_model(
            model, self.repository.select_recipe_items(recipe_id)
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="put /recipes/{recipe_id}/{item_id}",
            path={"recipe_id": "integer", "item_id": "integer"},
            responses=RecipeResponse,
            errors=[RecipeNotFoundError, ItemNotFoundError, LoggedOut],
        )
