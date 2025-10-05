from functools import wraps
from typing import Awaitable, Callable, ParamSpec, Protocol, TypeVar

from api.agent import Agent

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


class MethodLike(Protocol[P, R]):
    def __init__(self, agent: Agent) -> None: ...
    async def run(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


class Repository:
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def wrap(self, Method: type[MethodLike[P, R]]) -> Callable[P, Awaitable[R]]:
        m = Method(self.agent)

        @wraps(m.run)
        async def method(*args: P.args, **kwargs: P.kwargs) -> R:
            with self.agent:
                return await m.run(*args, **kwargs)

        return method
