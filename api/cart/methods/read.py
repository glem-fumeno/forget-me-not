from api.cart.models import CartItemResponse
from api.core.method import Method


class CartReadMethod(Method):
    async def run(self) -> list[CartItemResponse]:
        items = self.agent.items.select_many()
        item_ids = self.agent.cart.select_many()
        return [
            CartItemResponse(
                item_id=items[item_id].item_id,
                name=items[item_id].name,
                icon=items[item_id].icon,
                origin=origin,
            )
            for (item_id, origin) in item_ids
        ]
