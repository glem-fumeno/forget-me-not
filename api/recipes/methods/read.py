from fastapi import HTTPException

from api.core.method import Method
from api.items.models import ItemResponse
from api.recipes.models import RecipeResponse


class RecipeReadMethod(Method):
    async def run(self, recipe_id: int) -> RecipeResponse:
        result = self.agent.recipes.select(recipe_id)
        if result is None:
            raise HTTPException(404, "Recipe not found")
        items = self.agent.items.select_many()
        item_ids = self.agent.recipes.select_items(recipe_id)
        return RecipeResponse(
            recipe_id=result.recipe_id,
            name=result.name,
            icon=result.icon,
            items=[
                ItemResponse(
                    item_id=item_id,
                    name=items[item_id].name,
                    icon=items[item_id].icon,
                )
                for item_id in item_ids
            ],
        )
