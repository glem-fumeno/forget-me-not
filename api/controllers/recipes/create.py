from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.recipes.requests import RecipeCreateRequest
from api.models.recipes.responses import RecipeResponse


class RecipeCreateController(Controller):
    def run(self, request: RecipeCreateRequest) -> RecipeResponse:
        model = request.to_model()
        self.repository.recipes.insert_recipe(model)
        return RecipeResponse.from_model(model, [])

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /recipes/new",
            body=RecipeCreateRequest,
            responses=RecipeResponse,
            errors=[],
        )
