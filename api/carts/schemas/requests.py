from dataclasses import dataclass
from typing import Any

from api.carts.schemas.models import CartModel
from api.schemas import Request


@dataclass
class CartCreateRequest(Request):
    name: str
    icon: str

    def to_model(self) -> CartModel:
        return CartModel(-1, self.name, self.icon)

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
class CartUpdateRequest(Request):
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
