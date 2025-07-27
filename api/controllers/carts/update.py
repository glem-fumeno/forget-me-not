from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.carts.requests import CartUpdateRequest
from api.models.carts.responses import CartResponse


class CartUpdateController(CartController):
    def run(self, cart_id: int, request: CartUpdateRequest) -> CartResponse:
        self.validate_access()
        model = self.repository.carts.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        self.model = model
        self.cart_id = cart_id
        self.request = request

        self.update_name()
        self.update_icon()

        self.repository.carts.update_cart(self.model)
        items = self.repository.items.select_items()
        cart_items = self.repository.carts.select_cart_items(cart_id)
        return CartResponse.from_model(
            model, [(items[item], origin) for item, origin in cart_items]
        )

    def update_name(self):
        if self.request.name is None:
            return
        self.model.name = self.request.name

    def update_icon(self):
        if self.request.icon is None:
            return
        self.model.icon = self.request.icon

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="patch /carts/{cart_id}",
            path={"cart_id": "integer"},
            body=CartUpdateRequest,
            responses=CartResponse,
            errors=[CartNotFoundError, LoggedOut],
        )
