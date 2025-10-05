from api.agent import Agent
from api.cart.methods.add_recipe import CartAddRecipeMethod
from api.cart.methods.stream import CartStreamMethod
from api.core.repository import Repository
from api.cart.methods.read import CartReadMethod
from api.cart.methods.add_item import CartAddItemMethod
from api.cart.methods.remove_item import CartRemoveItemMethod


class CartRepository(Repository):
    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)

        self.read = self.wrap(CartReadMethod)
        self.stream = CartStreamMethod(agent).run
        self.add_item = self.wrap(CartAddItemMethod)
        self.add_recipe = self.wrap(CartAddRecipeMethod)
        self.remove_item = self.wrap(CartRemoveItemMethod)
