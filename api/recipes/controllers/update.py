from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.recipes.controllers.core import RecipeController
from api.recipes.schemas.errors import RecipeNotFoundError
from api.recipes.schemas.requests import RecipeUpdateRequest
from api.recipes.schemas.responses import RecipeResponse


class RecipeUpdateController(RecipeController):
    def run(
        self, recipe_id: int, request: RecipeUpdateRequest
    ) -> RecipeResponse:
        self.validate_access()
        model = self.repository.select_recipe(self.issuer.user_id, recipe_id)
        if model is None:
            raise RecipeNotFoundError
        self.model = model
        self.recipe_id = recipe_id
        self.request = request

        self.update_name()
        self.update_icon()

        self.repository.update_recipe(self.model)
        return RecipeResponse.from_model(
            model, self.repository.select_recipe_items(self.recipe_id)
        )

    def update_name(self):
        if self.request.name is None:
            return
        self.model.name = self.request.name

    def update_icon(self):
        if self.request.icon is None:
            return
        self.model.icon = self.request.icon

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="patch /recipes/{recipe_id}",
            path={"recipe_id": "integer"},
            body=RecipeUpdateRequest,
            responses=RecipeResponse,
            errors=[RecipeNotFoundError, LoggedOut],
        )
