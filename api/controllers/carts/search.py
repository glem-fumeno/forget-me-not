from api.controllers.carts.controller import CartController
from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.models.carts.responses import CartListResponse, CartResponse


class CartSearchController(CartController):
    def run(self) -> CartListResponse:
        self.validate_access()
        carts = self.repository.carts.select_carts(self.issuer.user_id)
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
            errors=[LoggedOut],
        )
