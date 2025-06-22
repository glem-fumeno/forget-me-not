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
            "name": "milk",
            "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
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
