from api.controllers.carts.core import CartController
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse
from api.docs.models import EndpointDict
from api.errors import LoggedOut


class CartReadController(CartController):
    def run(self, cart_id: int) -> CartResponse:
        self.validate_access()
        model = self.repository.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        return CartResponse.from_model(
            model, self.repository.select_cart_items(cart_id)
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /carts/{cart_id}",
            path={"cart_id": "integer"},
            responses=CartResponse,
            errors=[LoggedOut, CartNotFoundError],
        )
