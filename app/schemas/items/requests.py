from pydantic import Field

from app.schemas.items.models import ItemModel
from app.schemas.payload import Request


class ItemCreateRequest(Request):
    _docs_path = "items/create"
    name: str = Field(..., min_length=1, max_length=255)
    icon: str | None = Field(default=None, min_length=1, max_length=255)

    def to_model(self) -> ItemModel:
        return ItemModel(
            name=self.name,
            icon=self.icon,
            created_at=self.now,
            updated_at=self.now,
        )
