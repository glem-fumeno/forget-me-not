from api.agent import Agent
from api.core.repository import Repository
from api.files.methods.create import FileCreateMethod
from api.files.methods.delete import FileDeleteMethod
from api.files.methods.search import FileSearchMethod
from api.files.methods.update import FileUpdateMethod


class FileRepository(Repository):
    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)

        self.create = self.wrap(FileCreateMethod)
        self.search = self.wrap(FileSearchMethod)
        self.update = self.wrap(FileUpdateMethod)
        self.delete = self.wrap(FileDeleteMethod)
