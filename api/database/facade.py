import inspect
from sqlite3 import Cursor
from typing import Any

from api.context import Context


class Facade:
    def __init__(self, ctx: Context, cursor: Cursor) -> None:
        self.ctx = ctx
        self.cursor = cursor

    def __getattribute__(self, name: str, /) -> Any:
        field = object.__getattribute__(self, name)
        if (
            callable(field)
            and hasattr(field, "__qualname__")
            and field.__name__ == "run"
        ):
            r = inspect.getmodule(field)
            classname = field.__qualname__.removesuffix(".run")
            return getattr(r, classname)(self.ctx, self.cursor).run
        return field
