from app.schemas.items.exceptions import ItemNotFound
from app.schemas.items.responses import ItemResponse
from app.services.service import Service


class ItemReadService(Service):
    def __init__(self, item_id: int) -> None:
        self.item_id = item_id

    async def run(self) -> ItemResponse:
        model = await self.queries.items.select(self.item_id)
        if model is None:
            raise ItemNotFound
        return ItemResponse.from_model(model)
