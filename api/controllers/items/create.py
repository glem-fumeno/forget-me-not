from api.controllers.items.controller import ItemController
from api.docs.models import EndpointDict
from api.errors import Inaccessible, LoggedOut
from api.models.items.errors import ItemExistsError
from api.models.items.requests import ItemCreateRequest
from api.models.items.responses import ItemResponse


class ItemCreateController(ItemController):
    def run(self, request: ItemCreateRequest) -> ItemResponse:
        self.validate_access()
        duplicate = self.repository.items.select_item_by_name(request.name)
        if duplicate is not None:
            raise ItemExistsError
        model = request.to_model()
        self.repository.items.insert_item(model)
        return ItemResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /items/new",
            body=ItemCreateRequest,
            responses=ItemResponse,
            errors=[LoggedOut, Inaccessible, ItemExistsError],
        )
