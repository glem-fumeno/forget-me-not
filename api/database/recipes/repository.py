from api.database.facade import Facade
from api.database.recipes.delete_recipe import RecipeDeleteRecipeOperation
from api.database.recipes.delete_recipe_item import (
    RecipeDeleteRecipeItemOperation,
)
from api.database.recipes.insert_recipe import RecipeInsertRecipeOperation
from api.database.recipes.insert_recipe_item import (
    RecipeInsertRecipeItemOperation,
)
from api.database.recipes.select_recipe import RecipeSelectRecipeOperation
from api.database.recipes.select_recipe_items import (
    RecipeSelectRecipeItemsOperation,
)
from api.database.recipes.select_recipes import RecipeSelectRecipesOperation
from api.database.recipes.update_recipe import RecipeUpdateRecipeOperation


class RecipeRepository(Facade):
    insert_recipe = RecipeInsertRecipeOperation.run
    insert_recipe_item = RecipeInsertRecipeItemOperation.run
    select_recipes = RecipeSelectRecipesOperation.run
    select_recipe_items = RecipeSelectRecipeItemsOperation.run
    select_recipe = RecipeSelectRecipeOperation.run
    update_recipe = RecipeUpdateRecipeOperation.run
    delete_recipe = RecipeDeleteRecipeOperation.run
    delete_recipe_item = RecipeDeleteRecipeItemOperation.run
