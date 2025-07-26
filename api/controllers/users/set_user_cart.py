from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.users.responses import UserResponse


class CartSetUserCartController(CartController):
    def run(self, cart_id: int) -> UserResponse:
        self.validate_access()
        model = self.repository.carts.select_cart(self.issuer.user_id, cart_id)
        if model is None:
            raise CartNotFoundError

        self.repository.users.update_user_cart(self.issuer.user_id, cart_id)
        model = self.repository.users.select_user(self.issuer.user_id)
        assert model is not None
        return UserResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="put /users/cart/{cart_id}",
            path={"cart_id": "integer"},
            responses=UserResponse,
            errors=[CartNotFoundError, LoggedOut],
        )
