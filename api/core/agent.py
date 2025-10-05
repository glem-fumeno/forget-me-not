from functools import wraps
import sqlite3
from typing import Callable, ParamSpec, Protocol, TypeVar

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


class CallLike(Protocol[P, R]):
    def __init__(self, cursor: sqlite3.Cursor) -> None: ...
    def run(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


class Agent:

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor

    def wrap(self, Method: type[CallLike[P, R]]) -> Callable[P, R]:
        m = Method(self.cursor)

        @wraps(m.run)
        def method(*args: P.args, **kwargs: P.kwargs) -> R:
            return m.run(*args, **kwargs)

        return method
