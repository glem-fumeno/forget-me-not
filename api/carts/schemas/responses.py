from dataclasses import dataclass
from typing import Self

from api.carts.schemas.models import CartModel
from api.schemas import Response


@dataclass
class CartResponse(Response):
    cart_id: int
    name: str
    icon: str

    @classmethod
    def from_model(cls, model: CartModel) -> Self:
        return cls(model.cart_id, model.name, model.icon)

    @classmethod
    def get_example(cls) -> dict:
        return {
            "cart_id": 15,
            "name": "groceries",
            "icon": "https://img.icons8.com/pulsar-line/96/shopping-cart.png",
        }


@dataclass
class CartListResponse(Response):
    carts: list[CartResponse]
    count: int

    @classmethod
    def get_example(cls) -> dict:
        return {
            "carts": [
                {
                    "name": "groceries",
                    "icon": "https://img.icons8.com/pulsar-line/96/shopping-cart.png",
                },
                {
                    "name": "christmas",
                    "icon": "https://img.icons8.com/pulsar-line/96/christmas-tree.png",
                },
                {
                    "name": "shopping",
                    "icon": "https://img.icons8.com/pulsar-line/96/shopping-trolley.png",
                },
            ],
            "count": 3,
        }
