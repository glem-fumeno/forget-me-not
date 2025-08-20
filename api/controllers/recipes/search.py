from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.recipes.responses import RecipeListResponse, RecipeResponse


class RecipeSearchController(Controller):
    def run(self) -> RecipeListResponse:
        recipes = self.repository.recipes.select_recipes()
        recipe_list = list(recipes.values())
        recipes_items = self.repository.recipes.select_recipe_items(
            [recipe.recipe_id for recipe in recipe_list]
        )
        items = self.repository.items.select_items()
        return RecipeListResponse(
            recipes=[
                RecipeResponse.from_model(
                    model, [items[item_id] for item_id in recipe_items]
                )
                for model, recipe_items in zip(recipe_list, recipes_items)
            ],
            count=len(recipes),
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /recipes/search",
            responses=RecipeListResponse,
            errors=[],
        )
