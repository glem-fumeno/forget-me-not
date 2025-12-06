import json
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar

from fastapi import HTTPException
from pydantic import BaseModel

from app.config import get_config


class DocsObject(BaseModel):
    _docs_path: ClassVar[str | None] = None
    _docs: ClassVar[dict[str, Any]] = {}

    @classmethod
    def get_docs(cls) -> dict:
        if cls._docs_path is None:
            return {
                k: {"summary": k, "value": v} for k, v in cls._docs.items()
            }
        path = Path("docs").joinpath(cls._docs_path)
        config = get_config()
        return {
            file.stem: {
                "summary": file.stem,
                "value": json.loads(
                    file.read_text().replace("{API_URL}", config.API_URL)
                ),
            }
            for file in (sorted(path.iterdir()) if path.is_dir() else [path])
        }


class Response(DocsObject): ...


class Request(DocsObject):
    @property
    def now(self) -> datetime:
        return datetime.now()


class BasicResponse(Response):
    _docs = {"OK": {"message": "OK"}}
    message: str = "OK"


class APIException(HTTPException):
    CODE = 500
    DETAIL = "Internal Server error"

    def __init__(self) -> None:
        super().__init__(self.CODE, self.DETAIL)

    @classmethod
    def get_value(cls) -> Any:
        return {"detail": cls.DETAIL}
