from app.schemas.items.exceptions import ItemAlreadyExists
from app.schemas.items.requests import ItemCreateRequest
from app.schemas.items.responses import ItemResponse
from app.services.service import Service


class ItemCreateService(Service):
    def __init__(self, request: ItemCreateRequest) -> None:
        self.request = request

    async def run(self) -> ItemResponse:
        model = await self.queries.items.select_by_name(self.request.name)
        if model is not None:
            raise ItemAlreadyExists
        model = self.request.to_model()
        item_id = await self.queries.items.insert(model)
        model = await self.queries.items.select(item_id)
        assert model is not None
        return ItemResponse.from_model(model)
