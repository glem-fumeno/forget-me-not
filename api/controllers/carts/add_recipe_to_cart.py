from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse
from api.models.recipes.errors import RecipeNotFoundError


class CartAddRecipeToCartController(Controller):
    def run(self, cart_id: int, recipe_id: int) -> CartResponse:
        model = self.repository.carts.select_cart(cart_id)
        if model is None:
            raise CartNotFoundError
        recipe = self.repository.recipes.select_recipe(recipe_id)
        if recipe is None:
            raise RecipeNotFoundError
        item_ids = self.repository.recipes.select_recipe_items([recipe_id])

        self.repository.carts.insert_cart_items(
            cart_id, item_ids[0], recipe.name
        )
        items = self.repository.items.select_items()
        cart_items = self.repository.carts.select_cart_items(cart_id)
        return CartResponse.from_model(
            model, [(items[item], model) for item, model in cart_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="put /carts/{cart_id}/recipes/{recipe_id}",
            path={"cart_id": "integer", "recipe_id": "integer"},
            responses=CartResponse,
            errors=[CartNotFoundError, RecipeNotFoundError],
        )
