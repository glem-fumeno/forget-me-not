from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse
from api.models.items.errors import ItemNotFoundError


class CartRemoveFromCartController(CartController):
    def run(self, cart_id: int, item_id: int, origin: str) -> CartResponse:
        self.validate_access()
        model = self.repository.carts.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        items = self.repository.items.select_items()
        if item_id not in items:
            raise ItemNotFoundError

        self.repository.carts.delete_cart_item(cart_id, item_id, origin)
        cart_items = self.repository.carts.select_cart_items(cart_id)
        return CartResponse.from_model(
            model, [(items[item], origin) for item, origin in cart_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /carts/{cart_id}/{item_id}",
            path={"cart_id": "integer", "item_id": "integer"},
            query={"origin": "string"},
            responses=CartResponse,
            errors=[CartNotFoundError, ItemNotFoundError, LoggedOut],
        )
