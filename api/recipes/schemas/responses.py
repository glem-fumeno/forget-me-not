from typing import Self

from api.items.schemas.models import ItemModel
from api.items.schemas.responses import ItemResponse
from api.recipes.schemas.models import RecipeModel
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
            "name": "groceries",
            "icon": "https://img.icons8.com/pulsar-line/96/shopping-recipe.png",
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


class RecipeListResponse(Response):
    recipes: list[RecipeResponse]
    count: int

    @classmethod
    def get_example(cls) -> dict:
        return {
            "recipes": [
                {
                    "name": "groceries",
                    "icon": "https://img.icons8.com/pulsar-line/96/shopping-recipe.png",
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
