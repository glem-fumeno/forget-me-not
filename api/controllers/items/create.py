from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.items.errors import ItemExistsError
from api.models.items.requests import ItemCreateRequest
from api.models.items.responses import ItemResponse


class ItemCreateController(Controller):
    def run(self, request: ItemCreateRequest) -> ItemResponse:
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
            errors=[ItemExistsError],
        )
