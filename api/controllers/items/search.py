from api.docs.models import EndpointDict
from api.errors import LoggedOut
from api.controllers.items.core import ItemController
from api.models.items.responses import ItemListResponse, ItemResponse


class ItemSearchController(ItemController):
    def run(self) -> ItemListResponse:
        self.validate_access(admin=False)
        items = self.repository.select_items()
        return ItemListResponse(
            items=[ItemResponse.from_model(model) for model in items.values()],
            count=len(items),
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /items/search",
            responses=ItemListResponse,
            errors=[LoggedOut],
        )
