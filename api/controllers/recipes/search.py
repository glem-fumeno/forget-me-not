from api.controllers.recipes.controller import RecipeController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.recipes.responses import RecipeListResponse, RecipeResponse


class RecipeSearchController(RecipeController):
    def run(self) -> RecipeListResponse:
        self.validate_access()
        recipes = self.repository.recipes.select_recipes(self.issuer.user_id)
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
            errors=[LoggedOut],
        )
