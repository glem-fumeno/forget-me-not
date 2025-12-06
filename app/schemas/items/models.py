from datetime import datetime

from app.schemas.model import Model


class ItemModel(Model):
    item_id: int | None = None
    name: str | None = None
    icon: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
