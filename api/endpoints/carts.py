from flask import request

from api.controllers.carts.add_to_cart import CartAddToCartController
from api.controllers.carts.create import CartCreateController
from api.controllers.carts.delete import CartDeleteController
from api.controllers.carts.read import CartReadController
from api.controllers.carts.remove_from_cart import CartRemoveFromCartController
from api.controllers.carts.search import CartSearchController
from api.controllers.carts.update import CartUpdateController
from api.endpoints.endpoints import Endpoints
from api.models.carts.requests import CartCreateRequest, CartUpdateRequest


class CartEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__("carts", "/carts")
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
