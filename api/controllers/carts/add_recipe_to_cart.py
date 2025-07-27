from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse
from api.models.recipes.errors import RecipeNotFoundError


class CartAddRecipeToCartController(CartController):
    def run(self, cart_id: int, recipe_id: int) -> CartResponse:
        self.validate_access()
        model = self.repository.carts.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        recipe = self.repository.recipes.select_recipe(
            self.issuer.user_id, recipe_id
        )
        if recipe is None:
            raise RecipeNotFoundError
        item_ids = self.repository.recipes.select_recipe_items(recipe_id)

        self.repository.carts.insert_cart_items(cart_id, item_ids, recipe.name)
        items = self.repository.items.select_items()
        cart_items = self.repository.carts.select_cart_items(cart_id)
        return CartResponse.from_model(
            model, [(items[item], model) for item, model in cart_items.items()]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="put /carts/{cart_id}/recipes/{recipe_id}",
            path={"cart_id": "integer", "recipe_id": "integer"},
            responses=CartResponse,
            errors=[CartNotFoundError, RecipeNotFoundError, LoggedOut],
        )
