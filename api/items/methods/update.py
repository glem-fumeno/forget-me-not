from fastapi import HTTPException

from api.core.method import Method
from api.items.models import ItemModel, ItemRequest, ItemResponse


class ItemUpdateMethod(Method):
    async def run(self, item_id: int, request: ItemRequest) -> ItemResponse:
        item = self.agent.items.select(item_id)
        if item is None:
            raise HTTPException(404, "Item not found")
        duplicate = self.agent.items.select_by_name(request.name)
        if duplicate is not None and duplicate.item_id != item_id:
            raise HTTPException(409, "Item already exists")
        model = ItemModel(item_id, request.name, request.icon)
        self.agent.items.update(model)
        result = self.agent.items.select(item_id)
        assert result is not None
        return ItemResponse(
            item_id=result.item_id, name=result.name, icon=result.icon
        )
