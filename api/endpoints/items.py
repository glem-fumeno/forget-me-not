from flask import request

from api.endpoints.endpoints import Endpoints
from api.controllers.items.create import ItemCreateController
from api.controllers.items.delete import ItemDeleteController
from api.controllers.items.read import ItemReadController
from api.controllers.items.search import ItemSearchController
from api.controllers.items.update import ItemUpdateController
from api.database.items.core import ItemDatabaseRepository
from api.models.items.requests import ItemCreateRequest, ItemUpdateRequest


class ItemEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__("items", "/items", ItemDatabaseRepository)
        self.route("post /new", self.create)
        self.route("get /search", self.search)
        self.route("get /<item_id>", self.read)
        self.route("patch /<item_id>", self.update)
        self.route("delete /<item_id>", self.delete)

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
