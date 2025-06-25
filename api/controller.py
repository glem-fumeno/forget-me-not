from abc import ABC, abstractmethod
from typing import Protocol

from api.broker import Broker
from api.context import Context
from api.docs.models import EndpointDict


class Repository(Protocol): ...


class Controller(ABC):
    def __init__(self, ctx: Context, repository: Repository) -> None:
        self.repository = repository
        self.broker = Broker()
        self.ctx = ctx

    def publish(self, *args, **kwargs):
        self.broker.publish(self.ctx, self.__class__.__name__, *args, **kwargs)

    @classmethod
    @abstractmethod
    def get_docs(cls) -> EndpointDict: ...
