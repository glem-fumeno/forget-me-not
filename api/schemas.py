from abc import ABC, abstractmethod
from typing import Any, Self

from flask import Request as FlaskRequest
from pydantic import BaseModel


class Response(ABC, BaseModel):

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    @classmethod
    @abstractmethod
    def get_example(cls) -> Any: ...


class Request(ABC, BaseModel):

    @classmethod
    def from_flask(cls, request: FlaskRequest) -> Self:
        return cls.model_validate(request.get_json())

    @classmethod
    @abstractmethod
    def get_examples(cls) -> dict[str, Any]: ...


class Model(ABC, BaseModel):

    @classmethod
    def from_db(cls, description: tuple, result: tuple):
        assert len(description) == len(result), "description, result mismatch"
        keys = [column[:-1] for column, *_ in description]
        return cls.model_validate({k: v for k, v in zip(keys, result)})

    def copy(self) -> Self:
        return self.model_copy(deep=True)

    @property
    @abstractmethod
    def parameters(self) -> tuple: ...
