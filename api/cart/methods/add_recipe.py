from fastapi import HTTPException

from api.cart.models import CartItemResponse
from api.core.method import Method


class CartAddRecipeMethod(Method):
    async def run(self, recipe_id: int) -> list[CartItemResponse]:
        recipe = self.agent.recipes.select(recipe_id)
        if recipe is None:
            raise HTTPException(404, "Recipe not found")
        item_ids = self.agent.recipes.select_items(recipe_id)
        self.agent.cart.insert_many(recipe.name, item_ids)
        items = self.agent.items.select_many()
        item_ids = self.agent.cart.select_many()
        response = [
            CartItemResponse(
                item_id=items[item_id].item_id,
                name=items[item_id].name,
                icon=items[item_id].icon,
                origin=origin,
            )
            for (item_id, origin) in item_ids
        ]
        await self.agent.notify(response)
        return response
