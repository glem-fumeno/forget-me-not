from flask import request

from api.endpoints import Endpoints
from api.items.controllers.create import ItemCreateController
from api.items.controllers.delete import ItemDeleteController
from api.items.controllers.read import ItemReadController
from api.items.controllers.search import ItemSearchController
from api.items.controllers.update import ItemUpdateController
from api.items.database.core import ItemDatabaseRepository
from api.items.schemas.requests import ItemCreateRequest, ItemUpdateRequest


class ItemEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__("items", "/items", ItemDatabaseRepository())
        self.route("post /new", self.create, ItemCreateController)
        self.route("get /search", self.search, ItemSearchController)
        self.route("get /<item_id>", self.read, ItemReadController)
        self.route("patch /<item_id>", self.update, ItemUpdateController)
        self.route("delete /<item_id>", self.delete, ItemDeleteController)

    @Endpoints.handler
    def create(self, controller: ItemCreateController):
        return controller.run(ItemCreateRequest.from_flask(request))

    @Endpoints.handler
    def search(self, controller: ItemSearchController):
        return controller.run()

    @Endpoints.handler
    def read(self, controller: ItemReadController, item_id: int):
        return controller.run(item_id)

    @Endpoints.handler
    def update(self, controller: ItemUpdateController, item_id: int):
        return controller.run(item_id, ItemUpdateRequest.from_flask(request))

    @Endpoints.handler
    def delete(self, controller: ItemDeleteController, item_id: int):
        return controller.run(item_id)


endpoints = ItemEndpoints()
