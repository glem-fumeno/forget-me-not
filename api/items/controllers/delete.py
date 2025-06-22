from api.docs.models import EndpointDict
from api.errors import Inaccessible, LoggedOut
from api.items.controllers.core import ItemController
from api.items.schemas.errors import ItemNotFoundError
from api.items.schemas.responses import ItemResponse


class ItemDeleteController(ItemController):
    def run(self, item_id: int) -> ItemResponse:
        self.validate_access()
        model = self.repository.select_item(item_id)
        if model is None:
            raise ItemNotFoundError
        self.repository.delete_item(item_id)
        return ItemResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /items/{item_id}",
            path={"item_id": "integer"},
            responses=ItemResponse,
            errors=[LoggedOut, Inaccessible, ItemNotFoundError],
        )
