from flask import request

from api.carts.controllers.add_to_cart import CartAddToCartController
from api.carts.controllers.create import CartCreateController
from api.carts.controllers.delete import CartDeleteController
from api.carts.controllers.read import CartReadController
from api.carts.controllers.remove_from_cart import CartRemoveFromCartController
from api.carts.controllers.search import CartSearchController
from api.carts.controllers.update import CartUpdateController
from api.carts.database.core import CartDatabaseRepository
from api.carts.schemas.requests import CartCreateRequest, CartUpdateRequest
from api.endpoints import Endpoints


class CartEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__("carts", "/carts", CartDatabaseRepository)
        self.route("post /new", self.create)
        self.route("get /search", self.search)
        self.route("get /<cart_id>", self.read)
        self.route("patch /<cart_id>", self.update)
        self.route("delete /<cart_id>", self.delete)
        self.route("put /<cart_id>/<item_id>", self.add_to_cart)
        self.route("delete /<cart_id>/<item_id>", self.remove_from_cart)

    @Endpoints.handler
    def create(self, controller: CartCreateController):
        return controller.run(CartCreateRequest.from_flask(request))

    @Endpoints.handler
    def search(self, controller: CartSearchController):
        return controller.run()

    @Endpoints.handler
    def read(self, controller: CartReadController, cart_id: int):
        return controller.run(cart_id)

    @Endpoints.handler
    def update(self, controller: CartUpdateController, cart_id: int):
        return controller.run(cart_id, CartUpdateRequest.from_flask(request))

    @Endpoints.handler
    def delete(self, controller: CartDeleteController, cart_id: int):
        return controller.run(cart_id)

    @Endpoints.handler
    def add_to_cart(
        self, controller: CartAddToCartController, cart_id: int, item_id: int
    ):
        return controller.run(cart_id, item_id)

    @Endpoints.handler
    def remove_from_cart(
        self,
        controller: CartRemoveFromCartController,
        cart_id: int,
        item_id: int,
    ):
        return controller.run(cart_id, item_id)


endpoints = CartEndpoints()
