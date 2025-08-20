from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.carts.requests import CartCreateRequest
from api.models.carts.responses import CartResponse


class CartCreateController(Controller):
    def run(self, request: CartCreateRequest) -> CartResponse:
        model = request.to_model()
        self.repository.carts.insert_cart(model)
        return CartResponse.from_model(model, [])

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /carts/new",
            body=CartCreateRequest,
            responses=CartResponse,
            errors=[],
        )
