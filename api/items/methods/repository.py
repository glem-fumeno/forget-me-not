from api.agent import Agent
from api.core.repository import Repository
from api.items.methods.create import ItemCreateMethod
from api.items.methods.delete import ItemDeleteMethod
from api.items.methods.read import ItemReadMethod
from api.items.methods.search import ItemSearchMethod
from api.items.methods.update import ItemUpdateMethod


class ItemRepository(Repository):
    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)

        self.create = self.wrap(ItemCreateMethod)
        self.search = self.wrap(ItemSearchMethod)
        self.read = self.wrap(ItemReadMethod)
        self.update = self.wrap(ItemUpdateMethod)
        self.delete = self.wrap(ItemDeleteMethod)
