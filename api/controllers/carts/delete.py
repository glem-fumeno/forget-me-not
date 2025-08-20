from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse


class CartDeleteController(Controller):
    def run(self, cart_id: int) -> CartResponse:
        model = self.repository.carts.select_cart(cart_id)
        if model is None:
            raise CartNotFoundError
        items = self.repository.items.select_items()
        cart_items = self.repository.carts.select_cart_items(cart_id)
        self.repository.carts.delete_cart(cart_id)
        return CartResponse.from_model(
            model, [(items[item], origin) for item, origin in cart_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /carts/{cart_id}",
            path={"cart_id": "integer"},
            responses=CartResponse,
            errors=[CartNotFoundError],
        )
