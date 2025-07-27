from api.database.carts.delete_cart import CartDeleteCartOperation
from api.database.carts.delete_cart_item import CartDeleteCartItemOperation
from api.database.carts.delete_cart_user import CartDeleteCartUserOperation
from api.database.carts.insert_cart import CartInsertCartOperation
from api.database.carts.insert_cart_items import CartInsertCartItemsOperation
from api.database.carts.insert_cart_user import CartInsertCartUserOperation
from api.database.carts.select_cart import CartSelectCartOperation
from api.database.carts.select_cart_items import CartSelectCartItemsOperation
from api.database.carts.select_cart_users import CartSelectCartUsersOperation
from api.database.carts.select_carts import CartSelectCartsOperation
from api.database.carts.update_cart import CartUpdateCartOperation
from api.database.facade import Facade


class CartRepository(Facade):
    insert_cart = CartInsertCartOperation.run
    insert_cart_user = CartInsertCartUserOperation.run
    insert_cart_items = CartInsertCartItemsOperation.run
    select_carts = CartSelectCartsOperation.run
    select_cart_items = CartSelectCartItemsOperation.run
    select_cart_users = CartSelectCartUsersOperation.run
    select_cart = CartSelectCartOperation.run
    update_cart = CartUpdateCartOperation.run
    delete_cart = CartDeleteCartOperation.run
    delete_cart_item = CartDeleteCartItemOperation.run
    delete_cart_user = CartDeleteCartUserOperation.run
