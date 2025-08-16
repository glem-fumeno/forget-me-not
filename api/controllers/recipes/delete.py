from api.controllers.recipes.controller import RecipeController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.responses import RecipeResponse


class RecipeDeleteController(RecipeController):
    def run(self, recipe_id: int) -> RecipeResponse:
        self.validate_access()
        model = self.repository.recipes.select_recipe(
            self.issuer.user_id, recipe_id
        )
        if model is None:
            raise RecipeNotFoundError
        items = self.repository.items.select_items()
        recipe_items = self.repository.recipes.select_recipe_items([recipe_id])
        self.repository.recipes.delete_recipe_user(
            recipe_id, self.issuer.user_id
        )
        users = self.repository.recipes.select_recipe_users(recipe_id)
        if len(users) < 1:
            self.repository.recipes.delete_recipe(recipe_id)
        return RecipeResponse.from_model(
            model, [items[item] for item in recipe_items[0]]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /recipes/{recipe_id}",
            path={"recipe_id": "integer"},
            responses=RecipeResponse,
            errors=[LoggedOut, RecipeNotFoundError],
        )
