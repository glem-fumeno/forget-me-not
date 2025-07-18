from typing import Any

from api.models.carts.models import CartModel
from api.schemas import Request


class CartCreateRequest(Request):
    name: str
    icon: str

    def to_model(self) -> CartModel:
        return CartModel(cart_id=-1, name=self.name, icon=self.icon)

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "groceries": {
                "name": "groceries",
                "icon": "https://img.icons8.com/pulsar-line/96/shopping-cart.png",
            },
            "christmas": {
                "name": "christmas",
                "icon": "https://img.icons8.com/pulsar-line/96/christmas-tree.png",
            },
            "shopping": {
                "name": "shopping",
                "icon": "https://img.icons8.com/pulsar-line/96/shopping-trolley.png",
            },
        }


class CartUpdateRequest(Request):
    name: str | None = None
    icon: str | None = None

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "groceries": {
                "icon": "https://img.icons8.com/pulsar-line/96/fast-moving-consumer-goods.png",
            },
            "christmas": {
                "name": "x-mas",
            },
        }
