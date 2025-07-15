from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.controllers.items.core import ItemController
from api.models.items.errors import ItemNotFoundError
from api.models.items.responses import ItemResponse


class ItemReadController(ItemController):
    def run(self, item_id: int) -> ItemResponse:
        self.validate_access(admin=False)
        model = self.repository.select_item(item_id)
        if model is None:
            raise ItemNotFoundError
        return ItemResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /items/{item_id}",
            path={"item_id": "integer"},
            responses=ItemResponse,
            errors=[LoggedOut, ItemNotFoundError],
        )
