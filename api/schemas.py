from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, replace
from typing import Any, Self

from flask import Request as FlaskRequest


@dataclass
class Response(ABC):

    def to_dict(self) -> dict:
        return asdict(self, dict_factory=self.dict_factory)

    def dict_factory(self, items: list[tuple[str, Any]]) -> dict:
        return dict([(k, v) for k, v in items if v is not None])

    @classmethod
    @abstractmethod
    def get_example(cls) -> Any: ...


@dataclass
class Request(ABC):

    @classmethod
    def from_flask(cls, request: FlaskRequest) -> Self:
        return cls(**request.get_json())

    @classmethod
    @abstractmethod
    def get_examples(cls) -> dict[str, Any]: ...


@dataclass
class Model:

    def copy(self) -> Self:
        return replace(self)

    @property
    @abstractmethod
    def parameters(self) -> tuple: ...


class APIError(Exception):
    CODE = 500
    MESSAGE = "Internal Server Error"
