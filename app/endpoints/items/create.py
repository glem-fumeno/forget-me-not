from fastapi import APIRouter, Depends

from app.database.queries import QueriesDepends
from app.endpoints.endpoint import Endpoint
from app.schemas.items.exceptions import ItemAlreadyExists
from app.schemas.items.requests import ItemCreateRequest
from app.schemas.items.responses import ItemResponse
from app.services.items.create import ItemCreateService


class ItemCreateEndpoint(Endpoint, ItemCreateService):
    _request = ItemCreateRequest
    _response = ItemResponse
    _exceptions = [ItemAlreadyExists]

    @classmethod
    def attach_to_router(cls, router: APIRouter):
        @router.post("", **cls.get_detail())
        async def create_item(
            queries=QueriesDepends,
            instance: ItemCreateEndpoint = Depends(),
        ):
            return await instance.run(queries)

        return create_item
