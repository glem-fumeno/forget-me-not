from dataclasses import dataclass


@dataclass
class ItemModel:
    item_id: int
    name: str
    icon: str


@dataclass
class ItemRequest:
    name: str
    icon: str


@dataclass
class ItemResponse:
    item_id: int
    name: str
    icon: str
