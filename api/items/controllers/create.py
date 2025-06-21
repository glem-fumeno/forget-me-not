from api.docs.models import EndpointDict
from api.items.controllers.core import ItemController
from api.items.schemas.errors import ItemExistsError
from api.items.schemas.requests import ItemCreateRequest
from api.items.schemas.responses import ItemResponse


class ItemCreateController(ItemController):
    def run(self, request: ItemCreateRequest) -> ItemResponse:
        self.validate_access()
        duplicate = self.repository.select_item_by_name(request.name)
        if duplicate is not None:
            raise ItemExistsError
        model = request.to_model()
        self.repository.insert_item(model)
        return ItemResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /items/new",
            body=ItemCreateRequest,
            responses=ItemResponse,
            errors=[ItemExistsError],
        )
