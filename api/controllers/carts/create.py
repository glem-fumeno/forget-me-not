from api.controllers.carts.core import CartController
from api.models.carts.requests import CartCreateRequest
from api.models.carts.responses import CartResponse
from api.docs.models import EndpointDict
from api.errors import LoggedOut


class CartCreateController(CartController):
    def run(self, request: CartCreateRequest) -> CartResponse:
        self.validate_access()
        model = request.to_model()
        self.repository.insert_cart(self.issuer.user_id, model)
        return CartResponse.from_model(model, [])

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /carts/new",
            body=CartCreateRequest,
            responses=CartResponse,
            errors=[LoggedOut],
        )
