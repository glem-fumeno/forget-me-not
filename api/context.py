from __future__ import annotations

from typing import TypeAlias, TypeVar

ContextStorable: TypeAlias = int | float | str
T = TypeVar("T", bound=ContextStorable)


class Context:
    def __init__(
        self, store: dict[str, ContextStorable] | None = None
    ) -> None:
        if store is None:
            store = {}
        self.__store = store

    def get(self, key: str, default: T) -> T:
        result = self.__store.get(key, default)
        if type(result) != type(default):
            raise ValueError(
                f"Context type mismatch: {type(result)=} != {type(default)=}"
            )
        return result

    def add(self, key: str, value: ContextStorable) -> Context:
        self.__store[key] = value
        return self
