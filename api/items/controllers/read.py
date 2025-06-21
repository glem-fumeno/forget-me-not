from api.docs.models import EndpointDict
from api.items.controllers.core import ItemController
from api.items.schemas.errors import ItemNotFoundError
from api.items.schemas.responses import ItemResponse


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
            errors=[ItemNotFoundError],
        )
