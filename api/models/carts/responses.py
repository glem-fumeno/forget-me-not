from typing import Self

from api.models.carts.models import CartModel
from api.models.items.models import ItemModel
from api.models.items.responses import ItemResponse
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
                [
                    ItemResponse.from_model(item)
                    for item in sorted(items, key=lambda i: i.name)
                ]
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
                    "item_id": 1,
                    "name": "milk",
                    "icon": "https://img.icons8.com/pulsar-line/96/milk.png",
                },
                {
                    "item_id": 2,
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
                    "cart_id": 1,
                    "name": "groceries",
                    "icon": "https://img.icons8.com/pulsar-line/96/shopping-cart.png",
                },
                {
                    "cart_id": 2,
                    "name": "christmas",
                    "icon": "https://img.icons8.com/pulsar-line/96/christmas-tree.png",
                },
                {
                    "cart_id": 3,
                    "name": "shopping",
                    "icon": "https://img.icons8.com/pulsar-line/96/shopping-trolley.png",
                },
            ],
            "count": 3,
        }
