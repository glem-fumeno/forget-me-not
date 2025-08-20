from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.responses import RecipeResponse


class RecipeReadController(Controller):
    def run(self, recipe_id: int) -> RecipeResponse:
        model = self.repository.recipes.select_recipe(recipe_id)
        if model is None:
            raise RecipeNotFoundError
        items = self.repository.items.select_items()
        recipe_items = self.repository.recipes.select_recipe_items([recipe_id])
        return RecipeResponse.from_model(
            model, [items[item] for item in recipe_items[0]]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /recipes/{recipe_id}",
            path={"recipe_id": "integer"},
            responses=RecipeResponse,
            errors=[RecipeNotFoundError],
        )
