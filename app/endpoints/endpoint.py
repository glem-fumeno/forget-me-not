from typing import Any, Iterable, Self

from fastapi import APIRouter, Depends

from app.database.queries import Queries, QueriesDepends
from app.schemas.payload import APIException, BasicResponse, Request, Response
from app.services.service import Service


class Endpoint(Service):
    _request: type[Request] | None = None
    _response: type[Response] = BasicResponse
    _exceptions: Iterable[type[APIException]] = []
    _queries: Queries

    @classmethod
    def attach(cls, router: APIRouter, method: str, path: str):
        @router.api_route(path, methods=[method], **cls.get_detail())
        async def _(self=cls.depends()):
            return await self.connect(cls._queries).run()

    @classmethod
    def get_name(cls) -> str:
        result = ""
        for ch in cls.__name__.removesuffix("Endpoint"):
            if ch.isupper():
                result += " "
            result += ch
        words = []
        for word in result.split(" "):
            if len(words) > 0 and words[-1].isupper() and word.isupper():
                words[-1] += word
            else:
                words.append(word)
        return " ".join(words)

    @classmethod
    def query_depends(cls, queries=QueriesDepends):
        cls._queries = queries

    @classmethod
    def depends(cls) -> Self:
        return Depends(cls)

    @classmethod
    def get_examples(cls, value: Any) -> dict[str, Any]:
        return {"content": {"application/json": {"examples": value}}}

    @classmethod
    def get_detail(cls) -> dict[str, Any]:
        request_body = {}
        if cls._request is not None:
            request_body = {
                "requestBody": cls.get_examples(cls._request.get_docs())
            }

        return {
            "dependencies": [Depends(cls.query_depends)],
            "name": cls.get_name(),
            "response_model": cls._response,
            "response_model_exclude_none": True,
            "openapi_extra": {
                **request_body,
                "responses": {
                    200: cls.get_examples(
                        {
                            **cls._response.get_docs(),
                            **{
                                f"{exc.CODE} {exc.__name__}": {
                                    "value": exc.get_value()
                                }
                                for exc in cls._exceptions
                            },
                            **{
                                "422 ValidationException": {
                                    "value": [
                                        {
                                            "location": "location",
                                            "detail": "detail",
                                        }
                                    ]
                                }
                            },
                        },
                    )
                },
            },
        }
