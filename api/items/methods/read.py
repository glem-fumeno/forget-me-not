from fastapi import HTTPException

from api.core.method import Method
from api.items.models import ItemResponse


class ItemReadMethod(Method):
    async def run(self, item_id: int) -> ItemResponse:
        result = self.agent.items.select(item_id)
        if result is None:
            raise HTTPException(404, "Item not found")
        return ItemResponse(
            item_id=result.item_id, name=result.name, icon=result.icon
        )
