from loguru import logger

from api.broker import Broker
from api.context import Context
from api.database.repository import DatabaseRepository
from api.docs.models import EndpointDict


class Controller:
    def __init__(self, ctx: Context, repository: DatabaseRepository) -> None:
        self.repository = repository
        self.broker = Broker()
        self.ctx = ctx
        self.logger = logger.bind(hash=self.ctx.get("hash", "00000000"))
        self.logger.debug(f"Controller: {self.__class__.__name__}")

    def publish(self, *args, **kwargs):
        self.broker.publish(self.ctx, self.__class__.__name__, *args, **kwargs)

    @classmethod
    def get_docs(cls) -> EndpointDict:
        raise NotImplemented
