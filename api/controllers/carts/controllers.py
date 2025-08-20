from api.controllers.carts.add_recipe_to_cart import (
    CartAddRecipeToCartController,
)
from api.controllers.carts.add_to_cart import CartAddToCartController
from api.controllers.carts.create import CartCreateController
from api.controllers.carts.delete import CartDeleteController
from api.controllers.carts.read import CartReadController
from api.controllers.carts.read_default import CartReadDefaultController
from api.controllers.carts.remove_from_cart import CartRemoveFromCartController
from api.controllers.carts.search import CartSearchController
from api.controllers.carts.update import CartUpdateController
from api.controllers.carts.update_default import CartUpdateDefaultController
from api.controllers.facade import Facade


class CartControllers(Facade):
    add_recipe_to_cart = CartAddRecipeToCartController.run
    add_to_cart = CartAddToCartController.run
    create = CartCreateController.run
    delete = CartDeleteController.run
    read = CartReadController.run
    read_default = CartReadDefaultController.run
    remove_from_cart = CartRemoveFromCartController.run
    search = CartSearchController.run
    update = CartUpdateController.run
    update_default = CartUpdateDefaultController.run
