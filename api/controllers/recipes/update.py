from api.controllers.recipes.controller import RecipeController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.requests import RecipeUpdateRequest
from api.models.recipes.responses import RecipeResponse


class RecipeUpdateController(RecipeController):
    def run(
        self, recipe_id: int, request: RecipeUpdateRequest
    ) -> RecipeResponse:
        self.validate_access()
        model = self.repository.recipes.select_recipe(
            self.issuer.user_id, recipe_id
        )
        if model is None:
            raise RecipeNotFoundError
        self.model = model
        self.recipe_id = recipe_id
        self.request = request

        self.update_name()
        self.update_icon()

        self.repository.recipes.update_recipe(self.model)
        items = self.repository.items.select_items()
        recipe_items = self.repository.recipes.select_recipe_items(
            self.recipe_id
        )
        return RecipeResponse.from_model(
            model, [items[item] for item in recipe_items]
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
