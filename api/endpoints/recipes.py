from flask import request

from api.endpoints.endpoints import Endpoints
from api.controllers.recipes.add_to_recipe import RecipeAddToRecipeController
from api.controllers.recipes.create import RecipeCreateController
from api.controllers.recipes.delete import RecipeDeleteController
from api.controllers.recipes.read import RecipeReadController
from api.controllers.recipes.remove_from_recipe import (
    RecipeRemoveFromRecipeController,
)
from api.controllers.recipes.search import RecipeSearchController
from api.controllers.recipes.update import RecipeUpdateController
from api.database.recipes.core import RecipeDatabaseRepository
from api.models.recipes.requests import (
    RecipeCreateRequest,
    RecipeUpdateRequest,
)


class RecipeEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__("recipes", "/recipes", RecipeDatabaseRepository)
        self.route("post /new", self.create)
        self.route("get /search", self.search)
        self.route("get /<recipe_id>", self.read)
        self.route("patch /<recipe_id>", self.update)
        self.route("delete /<recipe_id>", self.delete)
        self.route("put /<recipe_id>/<item_id>", self.add_to_recipe)
        self.route("delete /<recipe_id>/<item_id>", self.remove_from_recipe)

    @Endpoints.handler
    def create(self, controller: RecipeCreateController):
        return controller.run(RecipeCreateRequest.from_flask(request))

    @Endpoints.handler
    def search(self, controller: RecipeSearchController):
        return controller.run()

    @Endpoints.handler
    def read(self, controller: RecipeReadController, recipe_id: int):
        return controller.run(recipe_id)

    @Endpoints.handler
    def update(self, controller: RecipeUpdateController, recipe_id: int):
        return controller.run(
            recipe_id, RecipeUpdateRequest.from_flask(request)
        )

    @Endpoints.handler
    def delete(self, controller: RecipeDeleteController, recipe_id: int):
        return controller.run(recipe_id)

    @Endpoints.handler
    def add_to_recipe(
        self,
        controller: RecipeAddToRecipeController,
        recipe_id: int,
        item_id: int,
    ):
        return controller.run(recipe_id, item_id)

    @Endpoints.handler
    def remove_from_recipe(
        self,
        controller: RecipeRemoveFromRecipeController,
        recipe_id: int,
        item_id: int,
    ):
        return controller.run(recipe_id, item_id)


endpoints = RecipeEndpoints()
