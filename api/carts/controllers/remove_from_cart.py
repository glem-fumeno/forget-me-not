from api.carts.controllers.core import CartController
from api.carts.schemas.errors import CartNotFoundError, ItemNotFoundError
from api.carts.schemas.responses import CartResponse
from api.docs.models import EndpointDict
from api.errors import LoggedOut


class CartRemoveFromCartController(CartController):
    def run(self, cart_id: int, item_id: int) -> CartResponse:
        self.validate_access()
        model = self.repository.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        items = self.repository.select_items()
        if item_id not in items:
            raise ItemNotFoundError

        self.repository.delete_cart_item(cart_id, item_id)
        return CartResponse.from_model(
            model, self.repository.select_cart_items(cart_id)
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /carts/{cart_id}/{item_id}",
            path={"cart_id": "integer", "item_id": "integer"},
            responses=CartResponse,
            errors=[CartNotFoundError, ItemNotFoundError, LoggedOut],
        )
