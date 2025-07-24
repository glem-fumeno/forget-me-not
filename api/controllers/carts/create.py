from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.requests import CartCreateRequest
from api.models.carts.responses import CartResponse


class CartCreateController(CartController):
    def run(self, request: CartCreateRequest) -> CartResponse:
        self.validate_access()
        model = request.to_model()
        self.repository.carts.insert_cart(self.issuer.user_id, model)
        return CartResponse.from_model(model, [])

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /carts/new",
            body=CartCreateRequest,
            responses=CartResponse,
            errors=[LoggedOut],
        )
