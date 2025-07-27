from api.controllers.facade import Facade
from api.controllers.recipes.add_to_recipe import RecipeAddToRecipeController
from api.controllers.recipes.add_user_to_recipe import (
    RecipeAddUserToRecipeController,
)
from api.controllers.recipes.create import RecipeCreateController
from api.controllers.recipes.delete import RecipeDeleteController
from api.controllers.recipes.read import RecipeReadController
from api.controllers.recipes.remove_from_recipe import (
    RecipeRemoveFromRecipeController,
)
from api.controllers.recipes.search import RecipeSearchController
from api.controllers.recipes.update import RecipeUpdateController


class RecipeControllers(Facade):
    add_user_to_recipe = RecipeAddUserToRecipeController.run
    create = RecipeCreateController.run
    read = RecipeReadController.run
    update = RecipeUpdateController.run
    delete = RecipeDeleteController.run
    search = RecipeSearchController.run
    add_to_recipe = RecipeAddToRecipeController.run
    remove_from_recipe = RecipeRemoveFromRecipeController.run
