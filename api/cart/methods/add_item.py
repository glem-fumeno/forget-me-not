from fastapi import HTTPException

from api.cart.models import CartItemResponse
from api.core.method import Method


class CartAddItemMethod(Method):
    async def run(self, item_id: int) -> list[CartItemResponse]:
        items = self.agent.items.select_many()
        if item_id not in items:
            raise HTTPException(404, "Item not found")
        self.agent.cart.insert_many("", {item_id})
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
