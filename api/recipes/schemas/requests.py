from typing import Any

from api.recipes.schemas.models import RecipeModel
from api.schemas import Request


class RecipeCreateRequest(Request):
    name: str
    icon: str

    def to_model(self) -> RecipeModel:
        return RecipeModel(recipe_id=-1, name=self.name, icon=self.icon)

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "groceries": {
                "name": "groceries",
                "icon": "https://img.icons8.com/pulsar-line/96/shopping-recipe.png",
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


class RecipeUpdateRequest(Request):
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
