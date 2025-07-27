from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.carts.responses import CartResponse
from api.models.users.errors import UserNotFoundError


class CartAddUserToCartController(CartController):
    def run(self, cart_id: int, user_id: int) -> CartResponse:
        self.validate_access()
        model = self.repository.carts.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError
        user = self.repository.users.select_user(user_id)
        if user is None:
            raise UserNotFoundError

        self.repository.carts.insert_cart_user(cart_id, user_id)
        items = self.repository.items.select_items()
        cart_items = self.repository.carts.select_cart_items(cart_id)
        return CartResponse.from_model(
            model, [(items[item], origin) for item, origin in cart_items]
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="put /carts/{cart_id}/users/{user_id}",
            path={"cart_id": "integer", "user_id": "integer"},
            responses=CartResponse,
            errors=[CartNotFoundError, UserNotFoundError, LoggedOut],
        )
