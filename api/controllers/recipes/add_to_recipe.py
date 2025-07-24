from api.controllers.recipes.controller import RecipeController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.items.errors import ItemNotFoundError
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.responses import RecipeResponse


class RecipeAddToRecipeController(RecipeController):
    def run(self, recipe_id: int, item_id: int) -> RecipeResponse:
        self.validate_access()
        model = self.repository.recipes.select_recipe(self.issuer.user_id, recipe_id)
        if model is None:
            raise RecipeNotFoundError
        items = self.repository.items.select_items()
        if item_id not in items:
            raise ItemNotFoundError

        self.repository.recipes.insert_recipe_item(recipe_id, item_id)
        recipe_items = self.repository.recipes.select_recipe_items(recipe_id)
        return RecipeResponse.from_model(
            model, [items[item] for item in recipe_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="put /recipes/{recipe_id}/{item_id}",
            path={"recipe_id": "integer", "item_id": "integer"},
            responses=RecipeResponse,
            errors=[RecipeNotFoundError, ItemNotFoundError, LoggedOut],
        )
