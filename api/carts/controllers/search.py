from api.docs.models import EndpointDict
from api.carts.controllers.core import CartController
from api.carts.schemas.responses import CartListResponse, CartResponse
from api.errors import LoggedOut


class CartSearchController(CartController):
    def run(self) -> CartListResponse:
        self.validate_access()
        carts = self.repository.select_carts(self.issuer.user_id)
        return CartListResponse(
            [CartResponse.from_model(model) for model in carts.values()],
            count=len(carts)
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /carts/search",
            responses=CartListResponse,
            errors=[LoggedOut],
        )
