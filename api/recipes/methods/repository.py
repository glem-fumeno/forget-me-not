from api.agent import Agent
from api.core.repository import Repository
from api.recipes.methods.add_item import RecipeAddItemMethod
from api.recipes.methods.create import RecipeCreateMethod
from api.recipes.methods.delete import RecipeDeleteMethod
from api.recipes.methods.read import RecipeReadMethod
from api.recipes.methods.remove_item import RecipeRemoveItemMethod
from api.recipes.methods.search import RecipeSearchMethod
from api.recipes.methods.update import RecipeUpdateMethod


class RecipeRepository(Repository):
    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)

        self.create = self.wrap(RecipeCreateMethod)
        self.add_item = self.wrap(RecipeAddItemMethod)
        self.search = self.wrap(RecipeSearchMethod)
        self.read = self.wrap(RecipeReadMethod)
        self.update = self.wrap(RecipeUpdateMethod)
        self.remove_item = self.wrap(RecipeRemoveItemMethod)
        self.delete = self.wrap(RecipeDeleteMethod)
