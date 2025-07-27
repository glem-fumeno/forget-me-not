from typing import Self

from api.models.carts.models import CartModel
from api.models.items.models import ItemModel
from api.models.items.responses import ItemResponse
from api.schemas import Response


class CartItemResponse(ItemResponse):
    origin: str | None

    @classmethod
    def from_model(cls, model: ItemModel, origin: str | None) -> Self:
        return cls(
            item_id=model.item_id,
            name=model.name,
            icon=model.icon,
            origin=origin,
        )


class CartResponse(Response):
    cart_id: int
    name: str
    icon: str
    items: list[CartItemResponse] | None

    @classmethod
    def from_model(
        cls,
        model: CartModel,
        items: list[tuple[ItemModel, str | None]] | None,
    ) -> Self:
        item_responses = None
        if items is not None:
            item_responses = [
                CartItemResponse.from_model(item, model)
                for item, model in items
            ]
            item_responses.sort(key=lambda i: i.name)
        return cls(
            cart_id=model.cart_id,
            name=model.name,
            icon=model.icon,
            items=item_responses,
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
