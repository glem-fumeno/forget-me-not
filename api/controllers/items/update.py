from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.items.errors import ItemExistsError, ItemNotFoundError
from api.models.items.requests import ItemUpdateRequest
from api.models.items.responses import ItemResponse


class ItemUpdateController(Controller):
    def run(self, item_id: int, request: ItemUpdateRequest) -> ItemResponse:
        model = self.repository.items.select_item(item_id)
        if model is None:
            raise ItemNotFoundError
        self.model = model
        self.item_id = item_id
        self.request = request

        self.update_name()
        self.update_icon()

        self.repository.items.update_item(self.model)
        return ItemResponse.from_model(model)

    def update_name(self):
        if self.request.name is None:
            return
        duplicate = self.repository.items.select_item_by_name(
            self.request.name
        )
        if duplicate is not None and duplicate != self.item_id:
            raise ItemExistsError
        self.model.name = self.request.name

    def update_icon(self):
        if self.request.icon is None:
            return
        self.model.icon = self.request.icon

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="patch /items/{item_id}",
            path={"item_id": "integer"},
            body=ItemUpdateRequest,
            responses=ItemResponse,
            errors=[ItemNotFoundError, ItemExistsError],
        )
