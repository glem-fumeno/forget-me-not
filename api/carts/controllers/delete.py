from api.carts.controllers.core import CartController
from api.carts.schemas.errors import CartNotFoundError
from api.carts.schemas.responses import CartResponse
from api.docs.models import EndpointDict
from api.errors import LoggedOut


class CartDeleteController(CartController):
    def run(self, cart_id: int) -> CartResponse:
        self.validate_access()
        model = self.repository.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        cart_items = self.repository.select_cart_items(cart_id)
        self.repository.delete_cart(cart_id)
        return CartResponse.from_model(model, cart_items)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /carts/{cart_id}",
            path={"cart_id": "integer"},
            responses=CartResponse,
            errors=[LoggedOut, CartNotFoundError],
        )
