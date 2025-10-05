from fastapi import HTTPException

from api.core.method import Method
from api.items.models import ItemResponse
from api.recipes.models import RecipeResponse


class RecipeAddItemMethod(Method):
    async def run(self, recipe_id: int, item_id: int) -> RecipeResponse:
        recipe = self.agent.recipes.select(recipe_id)
        if recipe is None:
            raise HTTPException(404, "Recipe not found")
        items = self.agent.items.select_many()
        if item_id not in items:
            raise HTTPException(404, "Item not found")
        self.agent.recipes.insert_item(recipe_id, item_id)
        item_ids = self.agent.recipes.select_items(recipe_id)
        return RecipeResponse(
            recipe_id=recipe.recipe_id,
            name=recipe.name,
            icon=recipe.icon,
            items=[
                ItemResponse(
                    item_id=item_id,
                    name=items[item_id].name,
                    icon=items[item_id].icon,
                )
                for item_id in item_ids
            ],
        )
