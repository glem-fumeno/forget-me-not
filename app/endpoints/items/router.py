from fastapi import APIRouter

from app.endpoints.items.create import ItemCreateEndpoint
from app.endpoints.items.read import ItemReadEndpoint

router = APIRouter(prefix="/items", tags=["Items"])

ItemCreateEndpoint.attach_to_router(router)
ItemReadEndpoint.attach_to_router(router)
