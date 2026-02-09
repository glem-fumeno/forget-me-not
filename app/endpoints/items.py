from fastapi import APIRouter

from app.endpoints.endpoint import Endpoint
from app.schemas.items.exceptions import ItemAlreadyExists, ItemNotFound
from app.schemas.items.requests import ItemCreateRequest
from app.schemas.items.responses import ItemResponse
from app.services.items.create import ItemCreateService
from app.services.items.read import ItemReadService


class ItemCreateEndpoint(Endpoint, ItemCreateService):
    _request = ItemCreateRequest
    _response = ItemResponse
    _exceptions = [ItemAlreadyExists]


class ItemReadEndpoint(Endpoint, ItemReadService):
    _response = ItemResponse
    _exceptions = [ItemNotFound]


router = APIRouter(prefix="/items", tags=["Items"])

ItemCreateEndpoint.attach(router, "post", "")
ItemReadEndpoint.attach(router, "get", "/{item_id:int}")
