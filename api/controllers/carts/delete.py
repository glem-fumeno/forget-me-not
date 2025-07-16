from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse


class CartDeleteController(CartController):
    def run(self, cart_id: int) -> CartResponse:
        self.validate_access()
        model = self.repository.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        items = self.repository.select_items()
        cart_items = self.repository.select_cart_items(cart_id)
        self.repository.delete_cart(cart_id)
        return CartResponse.from_model(
            model, [items[item] for item in cart_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /carts/{cart_id}",
            path={"cart_id": "integer"},
            responses=CartResponse,
            errors=[LoggedOut, CartNotFoundError],
        )
