from typing import Self

from api.models.items.models import ItemModel
from api.models.items.responses import ItemResponse
from api.models.recipes.models import RecipeModel
from api.schemas import Response


class RecipeResponse(Response):
    recipe_id: int
    name: str
    icon: str
    items: list[ItemResponse] | None

    @classmethod
    def from_model(
        cls, model: RecipeModel, items: list[ItemModel] | None
    ) -> Self:
        return cls(
            recipe_id=model.recipe_id,
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
            "recipe_id": 15,
            "name": "pancakes",
            "icon": "https://img.icons8.com/pulsar-line/96/pancake.png",
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


class RecipeListResponse(Response):
    recipes: list[RecipeResponse]
    count: int

    @classmethod
    def get_example(cls) -> dict:
        return {
            "recipes": [
                {
                    "recipe_id": 13,
                    "name": "pancakes",
                    "icon": "https://img.icons8.com/pulsar-line/96/pancake.png",
                },
                {
                    "recipe_id": 14,
                    "name": "omlette",
                    "icon": "https://img.icons8.com/pulsar-line/96/omlette.png",
                },
                {
                    "recipe_id": 15,
                    "name": "scrambled eggs",
                    "icon": "https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
                },
            ],
            "count": 3,
        }
