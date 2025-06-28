from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.recipes.controllers.core import RecipeController
from api.recipes.schemas.errors import ItemNotFoundError, RecipeNotFoundError
from api.recipes.schemas.responses import RecipeResponse


class RecipeRemoveFromRecipeController(RecipeController):
    def run(self, recipe_id: int, item_id: int) -> RecipeResponse:
        self.validate_access()
        model = self.repository.select_recipe(self.issuer.user_id, recipe_id)
        if model is None:
            raise RecipeNotFoundError
        items = self.repository.select_items()
        if item_id not in items:
            raise ItemNotFoundError

        self.repository.delete_recipe_item(recipe_id, item_id)
        return RecipeResponse.from_model(
            model, self.repository.select_recipe_items(recipe_id)
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /recipes/{recipe_id}/{item_id}",
            path={"recipe_id": "integer", "item_id": "integer"},
            responses=RecipeResponse,
            errors=[RecipeNotFoundError, ItemNotFoundError, LoggedOut],
        )
