from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.controllers.recipes.core import RecipeController
from api.models.recipes.responses import RecipeListResponse, RecipeResponse


class RecipeSearchController(RecipeController):
    def run(self) -> RecipeListResponse:
        self.validate_access()
        recipes = self.repository.select_recipes(self.issuer.user_id)
        return RecipeListResponse(
            recipes=[
                RecipeResponse.from_model(model, None)
                for model in recipes.values()
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
