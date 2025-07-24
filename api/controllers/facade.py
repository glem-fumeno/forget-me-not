
import inspect
from typing import Any
from api.context import Context
from api.controllers.repository import Repository


class Facade:
    def __init__(self, ctx: Context, repository: Repository) -> None:
        self.ctx = ctx
        self.repository = repository

    def __getattribute__(self, name: str, /) -> Any:
        field = object.__getattribute__(self, name)
        if (
            callable(field)
            and hasattr(field, "__qualname__")
            and field.__name__ == "run"
        ):
            r = inspect.getmodule(field)
            classname = field.__qualname__.removesuffix(".run")
            return getattr(r, classname)(self.ctx, self.repository).run
        return field
