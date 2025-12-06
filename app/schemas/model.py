from pydantic import BaseModel


def require[T](value: T | None) -> T:
    assert value is not None, f"value of type {type(value)} not set"
    return value


class Model(BaseModel): ...
