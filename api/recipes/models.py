from dataclasses import dataclass

from api.items.models import ItemResponse


@dataclass
class RecipeModel:
    recipe_id: int
    name: str
    icon: str


@dataclass
class RecipeRequest:
    name: str
    icon: str


@dataclass
class RecipeResponse:
    recipe_id: int
    name: str
    icon: str
    items: list[ItemResponse]
