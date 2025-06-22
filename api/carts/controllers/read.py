from api.docs.models import EndpointDict
from api.carts.controllers.core import CartController
from api.carts.schemas.errors import CartNotFoundError
from api.carts.schemas.responses import CartResponse


class CartReadController(CartController):
    def run(self, cart_id: int) -> CartResponse:
        self.validate_access()
        model = self.repository.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        return CartResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /carts/{cart_id}",
            path={"cart_id": "integer"},
            responses=CartResponse,
            errors=[CartNotFoundError],
        )
