from app.database.queries import Queries
from app.schemas.items.exceptions import ItemAlreadyExists
from app.schemas.items.requests import ItemCreateRequest
from app.schemas.items.responses import ItemResponse


class ItemCreateService:
    def __init__(self, request: ItemCreateRequest) -> None:
        self.request = request

    async def run(self, queries: Queries) -> ItemResponse:
        model = await queries.items.select_by_name(self.request.name)
        if model is not None:
            raise ItemAlreadyExists
        model = self.request.to_model()
        item_id = await queries.items.insert(model)
        model = await queries.items.select(item_id)
        assert model is not None
        return ItemResponse.from_model(model)
