from api.agent import Agent
from api.cart.methods.repository import CartRepository
from api.files.methods.repository import FileRepository
from api.items.methods.repository import ItemRepository
from api.recipes.methods.repository import RecipeRepository


class Repository:
    def __init__(self, agent: Agent) -> None:
        self.items = ItemRepository(agent)
        self.recipes = RecipeRepository(agent)
        self.cart = CartRepository(agent)
        self.files = FileRepository(agent)
