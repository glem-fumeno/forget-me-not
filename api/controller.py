from typing import Protocol
from api.broker import Broker
from api.context import Context
import random


class Repository(Protocol): ...

class Controller:
    def __init__(self) -> None:
        self.broker = Broker()
        self.ctx = Context().add("hash", f"{random.getrandbits(32):08x}")

    def publish(self, *args, **kwargs):
        self.broker.publish(self.ctx, self.__class__.__name__, *args, **kwargs)
