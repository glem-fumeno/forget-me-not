from fastapi import APIRouter, Depends

from app.database.queries import QueriesDepends
from app.endpoints.endpoint import Endpoint
from app.schemas.items.exceptions import (
    ItemNotFound,
)
from app.schemas.items.responses import ItemResponse
from app.services.items.read import ItemReadService


class ItemReadEndpoint(Endpoint, ItemReadService):
    _response = ItemResponse
    _exceptions = [ItemNotFound]

    @classmethod
    def attach_to_router(cls, router: APIRouter):
        @router.get("/{item_id:int}", **cls.get_detail())
        async def read_item(
            queries=QueriesDepends, instance: ItemReadEndpoint = Depends()
        ):
            return await instance.run(queries)

        return read_item
