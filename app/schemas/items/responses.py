from datetime import datetime
from typing import Self

from app.schemas.items.models import ItemModel
from app.schemas.model import require
from app.schemas.payload import Response


class ItemResponse(Response):
    _docs_path = "items/responses"
    item_id: int
    name: str
    icon: str | None = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, model: ItemModel) -> Self:
        return cls(
            item_id=require(model.item_id),
            name=require(model.name),
            icon=model.icon,
            created_at=require(model.created_at),
            updated_at=require(model.updated_at),
        )
