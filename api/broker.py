from typing import Callable

from api.context import Context
from api.singleton import Singleton


class Broker(metaclass=Singleton):
    def __init__(self) -> None:
        self.reset()

    def subscribe(self, subscriber: str, event: str, callback: Callable):
        if event not in self.callbacks:
            self.callbacks[event] = {}
        self.callbacks[event][subscriber] = callback

    def publish(self, ctx: Context, event: str, *args, **kwargs):
        for callback in self.callbacks.get(event, {}).values():
            callback(ctx, *args, **kwargs)

    def reset(self):
        self.callbacks = {}
