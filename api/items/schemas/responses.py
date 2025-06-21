from dataclasses import dataclass
from typing import Self

from api.schemas import Response
from api.items.schemas.models import ItemModel


@dataclass
class ItemResponse(Response):
    item_id: int
    name: str
    icon: str

    @classmethod
    def from_model(cls, model: ItemModel) -> Self:
        return cls(model.item_id, model.name, model.icon)

    @classmethod
    def get_example(cls) -> dict:
        return {
            "item_id": 15,
            "name": "milk",
            "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
        }
