from dataclasses import dataclass
from typing import Any

from api.items.schemas.models import ItemModel
from api.schemas import Request


@dataclass
class ItemCreateRequest(Request):
    name: str
    icon: str

    def to_model(self) -> ItemModel:
        return ItemModel(-1, self.name, self.icon)

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "milk": {
                "name": "milk",
                "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
            },
            "rice": {
                "name": "rice",
                "icon": "https://img.icons8.com/pulsar-line/96/rice-bowl.png",
            },
            "soap": {
                "name": "soap",
                "icon": "https://img.icons8.com/pulsar-line/96/soap.png",
            },
        }


@dataclass
class ItemUpdateRequest(Request):
    name: str | None = None
    icon: str | None = None

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "milk": {
                "icon": "https://img.icons8.com/pulsar-line/96/milk-carton.png",
            },
            "rice": {
                "name": "rice-bowl",
            },
        }
