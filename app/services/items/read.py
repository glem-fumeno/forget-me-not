from app.database.queries import Queries
from app.schemas.items.exceptions import ItemNotFound
from app.schemas.items.responses import ItemResponse


class ItemReadService:
    def __init__(self, item_id: int) -> None:
        self.item_id = item_id

    async def run(self, queries: Queries) -> ItemResponse:
        model = await queries.items.select(self.item_id)
        if model is None:
            raise ItemNotFound
        return ItemResponse.from_model(model)
