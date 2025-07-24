from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse


class CartReadUserCartController(CartController):
    def run(self) -> CartResponse:
        self.validate_access()
        cart_id = self.repository.carts.select_user_cart(self.issuer.user_id)
        if cart_id is None:
            raise CartNotFoundError
        model = self.repository.carts.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError

        items = self.repository.items.select_items()
        cart_items = self.repository.carts.select_cart_items(cart_id)
        return CartResponse.from_model(
            model, [items[item_id] for item_id in cart_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /users/cart",
            responses=CartResponse,
            errors=[CartNotFoundError, LoggedOut],
        )
