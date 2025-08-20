import inspect
from typing import Any

from api.context import Context
from api.database.repository import DatabaseRepository


class Facade:
    def __init__(self, ctx: Context, repository: DatabaseRepository) -> None:
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
