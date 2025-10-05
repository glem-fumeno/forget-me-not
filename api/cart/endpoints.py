from fastapi import APIRouter

from api.repository import Repository


class CartEndpoints:
    def __init__(self, repository: Repository) -> None:
        router = APIRouter(prefix="/cart")
        cart = repository.cart
        self.router = router

        router.get("/stream")(cart.stream)
        router.get("/items")(cart.read)
        router.put("/recipes/{recipe_id}")(cart.add_recipe)
        router.put("/items/{item_id}")(cart.add_item)
        router.delete("/items/{item_id}")(cart.remove_item)
