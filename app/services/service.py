from abc import ABC, abstractmethod

from app.database.queries import Queries


class Service(ABC):
    __queries: Queries | None = None

    @abstractmethod
    async def run(self): ...

    def connect(self, queries: Queries):
        self.__queries = queries
        return self

    @property
    def queries(self) -> Queries:
        assert self.__queries is not None, "Queries not set"
        return self.__queries
