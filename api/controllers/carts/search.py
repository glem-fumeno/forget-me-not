from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.carts.responses import CartListResponse, CartResponse


class CartSearchController(Controller):
    def run(self) -> CartListResponse:
        carts = self.repository.carts.select_carts()
        return CartListResponse(
            carts=[
                CartResponse.from_model(model, None)
                for model in carts.values()
            ],
            count=len(carts),
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /carts/search",
            responses=CartListResponse,
            errors=[],
        )
