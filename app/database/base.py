from typing import ParamSpec, Protocol, TypeVar

from aiosqlite import Connection

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


class CallLike(Protocol[P, R]):
    def __init__(self, connection: Connection) -> None: ...
    def run(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


class QueriesBase:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def wrap(self, method: type[CallLike[P, R]]):
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            return method(self.connection).run(*args, **kwargs)

        return wrapped
