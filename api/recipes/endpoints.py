from fastapi import APIRouter

from api.repository import Repository


class RecipeEndpoints:
    def __init__(self, repository: Repository) -> None:
        router = APIRouter(prefix="/recipes")
        recipes = repository.recipes
        self.router = router

        router.post("")(recipes.create)
        router.get("")(recipes.search)
        router.get("/{recipe_id}")(recipes.read)
        router.put("/{recipe_id}")(recipes.update)
        router.delete("/{recipe_id}")(recipes.delete)
        router.put("/{recipe_id}/{item_id}")(recipes.add_item)
        router.delete("/{recipe_id}/{item_id}")(recipes.remove_item)
