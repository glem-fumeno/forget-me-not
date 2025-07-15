from typing import Self

from api.items.schemas.models import ItemModel
from api.schemas import Response


class ItemResponse(Response):
    item_id: int
    name: str
    icon: str

    @classmethod
    def from_model(cls, model: ItemModel) -> Self:
        return cls(item_id=model.item_id, name=model.name, icon=model.icon)

    @classmethod
    def get_example(cls) -> dict:
        return {
            "item_id": 15,
            "name": "milk",
            "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
        }


class ItemListResponse(Response):
    items: list[ItemResponse]
    count: int

    @classmethod
    def get_example(cls) -> dict:
        return {
            "items": [
                {
                    "item_id": 1,
                    "name": "milk",
                    "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
                },
                {
                    "item_id": 2,
                    "name": "rice",
                    "icon": "https://img.icons8.com/pulsar-line/96/rice-bowl.png",
                },
                {
                    "item_id": 3,
                    "name": "soap",
                    "icon": "https://img.icons8.com/pulsar-line/96/soap.png",
                },
            ],
            "count": 3,
        }
