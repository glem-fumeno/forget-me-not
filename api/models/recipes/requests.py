from typing import Any

from api.models.recipes.models import RecipeModel
from api.schemas import Request


class RecipeCreateRequest(Request):
    name: str
    icon: str

    def to_model(self) -> RecipeModel:
        return RecipeModel(recipe_id=-1, name=self.name, icon=self.icon)

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "pancakes": {
                "name": "pancakes",
                "icon": "https://img.icons8.com/pulsar-line/96/pancake.png",
            },
            "omlette": {
                "name": "omlette",
                "icon": "https://img.icons8.com/pulsar-line/96/omlette.png",
            },
            "scrambled eggs": {
                "name": "scrambled eggs",
                "icon": "https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
            },
        }


class RecipeUpdateRequest(Request):
    name: str | None = None
    icon: str | None = None

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "name": {
                "name": "pancake stack",
            },
            "icon": {
                "icon": "https://img.icons8.com/pulsar-line/96/american-pancakes.png",
            },
        }
