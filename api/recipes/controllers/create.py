from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.recipes.controllers.core import RecipeController
from api.recipes.schemas.requests import RecipeCreateRequest
from api.recipes.schemas.responses import RecipeResponse


class RecipeCreateController(RecipeController):
    def run(self, request: RecipeCreateRequest) -> RecipeResponse:
        self.validate_access()
        model = request.to_model()
        self.repository.insert_recipe(self.issuer.user_id, model)
        return RecipeResponse.from_model(model, [])

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /recipes/new",
            body=RecipeCreateRequest,
            responses=RecipeResponse,
            errors=[LoggedOut],
        )
