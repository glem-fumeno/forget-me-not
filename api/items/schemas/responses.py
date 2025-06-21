from dataclasses import dataclass
from typing import Self

from api.items.schemas.models import ItemModel
from api.schemas import Response


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


@dataclass
class ItemListResponse(Response):
    items: list[ItemResponse]
    count: int

    @classmethod
    def get_example(cls) -> dict:
        return {
            "items": [
                {
                    "name": "milk",
                    "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
                },
                {
                    "name": "rice",
                    "icon": "https://img.icons8.com/pulsar-line/96/rice-bowl.png",
                },
                {
                    "name": "soap",
                    "icon": "https://img.icons8.com/pulsar-line/96/soap.png",
                },
            ],
            "count": 3,
        }
