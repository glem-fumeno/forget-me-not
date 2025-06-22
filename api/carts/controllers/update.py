from api.carts.controllers.core import CartController
from api.carts.schemas.errors import CartNotFoundError
from api.carts.schemas.requests import CartUpdateRequest
from api.carts.schemas.responses import CartResponse
from api.docs.models import EndpointDict
from api.errors import LoggedOut


class CartUpdateController(CartController):
    def run(self, cart_id: int, request: CartUpdateRequest) -> CartResponse:
        self.validate_access()
        model = self.repository.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        self.model = model
        self.cart_id = cart_id
        self.request = request

        self.update_name()
        self.update_icon()

        self.repository.update_cart(self.model)
        return CartResponse.from_model(
            model, self.repository.select_cart_items(self.cart_id)
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
