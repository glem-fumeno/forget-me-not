from api.database.carts.delete_cart import CartDeleteCartOperation
from api.database.carts.delete_cart_item import CartDeleteCartItemOperation
from api.database.carts.insert_cart import CartInsertCartOperation
from api.database.carts.insert_cart_items import CartInsertCartItemsOperation
from api.database.carts.insert_cart_user import CartInsertCartUserOperation
from api.database.carts.select_cart import CartSelectCartOperation
from api.database.carts.select_cart_items import CartSelectCartItemsOperation
from api.database.carts.select_carts import CartSelectCartsOperation
from api.database.carts.select_user_cart import CartSelectUserCartOperation
from api.database.carts.update_cart import CartUpdateCartOperation
from api.database.carts.update_user_cart import CartUpdateUserCartOperation
from api.database.facade import Facade


class CartRepository(Facade):
    insert_cart = CartInsertCartOperation.run
    insert_cart_user = CartInsertCartUserOperation.run
    insert_cart_items = CartInsertCartItemsOperation.run
    select_carts = CartSelectCartsOperation.run
    select_cart_items = CartSelectCartItemsOperation.run
    select_cart = CartSelectCartOperation.run
    select_user_cart = CartSelectUserCartOperation.run
    update_cart = CartUpdateCartOperation.run
    update_user_cart = CartUpdateUserCartOperation.run
    delete_cart = CartDeleteCartOperation.run
    delete_cart_item = CartDeleteCartItemOperation.run
