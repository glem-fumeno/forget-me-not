from typing import Literal, NotRequired, TypedDict

from api.errors import APIError
from api.schemas import Request, Response

DocTypeLiteral = Literal["string", "integer", "number", "boolean"]

EndpointDict = TypedDict(
    "EndpointDict",
    {
        "endpoint": str,
        "path": NotRequired[dict[str, DocTypeLiteral]],
        "query": NotRequired[dict[str, DocTypeLiteral]],
        "body": NotRequired[type[Request]],
        "responses": type[Response],
        "errors": list[type[APIError]],
    },
)
