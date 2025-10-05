from fastapi import HTTPException
from api.core.method import Method
from api.items.models import ItemModel, ItemRequest, ItemResponse


class ItemCreateMethod(Method):
    async def run(self, request: ItemRequest) -> ItemResponse:
        model = ItemModel(item_id=-1, name=request.name, icon=request.icon)
        duplicate = self.agent.items.select_by_name(request.name)
        if duplicate is not None:
            raise HTTPException(409, "Item already exists")
        self.agent.items.insert(model)
        result = self.agent.items.select(model.item_id)
        assert result is not None, "could not insert item"
        return ItemResponse(
            item_id=result.item_id, name=result.name, icon=result.icon
        )
