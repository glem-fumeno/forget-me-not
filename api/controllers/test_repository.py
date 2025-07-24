from typing import Any


class TestRepository:
    def __init__(self, parent) -> None:
        object.__setattr__(self, "parent", parent)

    def __getattribute__(self, name: str, /) -> Any:
        parent = object.__getattribute__(self, "parent")
        try:
            field = object.__getattribute__(self, name)
        except Exception as e:
            print(e)
            field = object.__getattribute__(parent, name)
        return field

    def __setattr__(self, name: str, value: Any, /) -> None:
        parent = object.__getattribute__(self, "parent")
        if parent is None:
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(parent, name, value)
