from api.controllers.recipes.controller import RecipeController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.responses import RecipeResponse
from api.models.users.errors import UserNotFoundError


class RecipeAddUserToRecipeController(RecipeController):
    def run(self, recipe_id: int, user_id: int) -> RecipeResponse:
        self.validate_access()
        model = self.repository.recipes.select_recipe(
            self.issuer.user_id, recipe_id
        )
        if model is None:
            raise RecipeNotFoundError
        user = self.repository.users.select_user(user_id)
        if user is None:
            raise UserNotFoundError

        self.repository.recipes.insert_recipe_user(recipe_id, user_id)
        items = self.repository.items.select_items()
        recipe_items = self.repository.recipes.select_recipe_items([recipe_id])
        return RecipeResponse.from_model(
            model, [items[item] for item in recipe_items[0]]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="put /recipes/{recipe_id}/users/{user_id}",
            path={"recipe_id": "integer", "user_id": "integer"},
            responses=RecipeResponse,
            errors=[RecipeNotFoundError, UserNotFoundError, LoggedOut],
        )
