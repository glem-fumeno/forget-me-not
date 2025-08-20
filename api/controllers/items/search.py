from api.controllers.controller import Controller
from api.docs.models import EndpointDict
from api.models.items.responses import ItemListResponse, ItemResponse


class ItemSearchController(Controller):
    def run(self) -> ItemListResponse:
        items = self.repository.items.select_items()
        return ItemListResponse(
            items=[ItemResponse.from_model(model) for model in items.values()],
            count=len(items),
        )

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /items/search",
            responses=ItemListResponse,
            errors=[],
        )
