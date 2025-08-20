from api.database.carts.delete_cart import CartDeleteCartOperation
from api.database.carts.delete_cart_item import CartDeleteCartItemOperation
from api.database.carts.insert_cart import CartInsertCartOperation
from api.database.carts.insert_cart_items import CartInsertCartItemsOperation
from api.database.carts.select_cart import CartSelectCartOperation
from api.database.carts.select_cart_items import CartSelectCartItemsOperation
from api.database.carts.select_carts import CartSelectCartsOperation
from api.database.carts.select_default_cart import (
    CartSelectDefaultCartOperation,
)
from api.database.carts.update_cart import CartUpdateCartOperation
from api.database.carts.update_default_cart import (
    CartUpdateDefaultCartOperation,
)
from api.database.facade import Facade


class CartRepository(Facade):
    insert_cart = CartInsertCartOperation.run
    insert_cart_items = CartInsertCartItemsOperation.run
    select_carts = CartSelectCartsOperation.run
    select_cart_items = CartSelectCartItemsOperation.run
    select_default_cart = CartSelectDefaultCartOperation.run
    select_cart = CartSelectCartOperation.run
    update_cart = CartUpdateCartOperation.run
    update_default_cart = CartUpdateDefaultCartOperation.run
    delete_cart = CartDeleteCartOperation.run
    delete_cart_item = CartDeleteCartItemOperation.run
