from fastapi import HTTPException

from api.core.method import Method
from api.items.models import ItemResponse
from api.recipes.models import RecipeModel, RecipeRequest, RecipeResponse


class RecipeUpdateMethod(Method):
    async def run(
        self, recipe_id: int, request: RecipeRequest
    ) -> RecipeResponse:
        recipe = self.agent.recipes.select(recipe_id)
        if recipe is None:
            raise HTTPException(404, "Recipe not found")
        duplicate = self.agent.recipes.select_by_name(request.name)
        if duplicate is not None and duplicate.recipe_id != recipe_id:
            raise HTTPException(409, "Recipe already exists")
        model = RecipeModel(recipe_id, request.name, request.icon)
        self.agent.recipes.update(model)
        result = self.agent.recipes.select(recipe_id)
        assert result is not None
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
