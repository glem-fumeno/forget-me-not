from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.items.errors import ItemNotFoundError
from api.models.items.responses import ItemResponse


class ItemDeleteController(Controller):
    def run(self, item_id: int) -> ItemResponse:
        model = self.repository.items.select_item(item_id)
        if model is None:
            raise ItemNotFoundError
        self.repository.items.delete_item(item_id)
        return ItemResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /items/{item_id}",
            path={"item_id": "integer"},
            responses=ItemResponse,
            errors=[ItemNotFoundError],
        )
