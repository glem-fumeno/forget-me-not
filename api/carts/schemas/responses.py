from typing import Self

from api.carts.schemas.models import CartModel
from api.items.schemas.models import ItemModel
from api.items.schemas.responses import ItemResponse
from api.schemas import Response


class CartResponse(Response):
    cart_id: int
    name: str
    icon: str
    items: list[ItemResponse] | None

    @classmethod
    def from_model(
        cls, model: CartModel, items: list[ItemModel] | None
    ) -> Self:
        return cls(
            cart_id=model.cart_id,
            name=model.name,
            icon=model.icon,
            items=(
                [ItemResponse.from_model(item) for item in items]
                if items is not None
                else None
            ),
        )

    @classmethod
    def get_example(cls) -> dict:
        return {
            "cart_id": 15,
            "name": "groceries",
            "icon": "https://img.icons8.com/pulsar-line/96/shopping-cart.png",
            "items": [
                {
                    "name": "milk",
                    "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
                },
                {
                    "name": "rice",
                    "icon": "https://img.icons8.com/pulsar-line/96/rice-bowl.png",
                },
            ],
        }


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
