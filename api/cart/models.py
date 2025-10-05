from dataclasses import dataclass
from api.items.models import ItemResponse


@dataclass
class CartItemResponse(ItemResponse):
    origin: str
