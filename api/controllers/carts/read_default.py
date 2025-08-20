from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse


class CartReadDefaultController(Controller):
    def run(self) -> CartResponse:
        model = self.repository.carts.select_default_cart()
        if model is None:
            raise CartNotFoundError
        items = self.repository.items.select_items()
        cart_items = self.repository.carts.select_cart_items(model.cart_id)
        return CartResponse.from_model(
            model, [(items[item], origin) for item, origin in cart_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /carts/default",
            responses=CartResponse,
            errors=[CartNotFoundError],
        )
