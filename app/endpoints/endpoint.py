from typing import Any, Iterable

from app.schemas.payload import APIException, BasicResponse, Request, Response


class Endpoint:
    _request: type[Request] | None = None
    _response: type[Response] = BasicResponse
    _exceptions: Iterable[type[APIException]] = []

    @classmethod
    def get_detail(cls) -> dict[str, Any]:
        request_body = {}
        if cls._request is not None:
            request_body = {
                "requestBody": {
                    "content": {
                        "application/json": {
                            "examples": cls._request.get_docs()
                        }
                    }
                }
            }

        return {
            "response_model": cls._response,
            "response_model_exclude_none": True,
            "openapi_extra": {
                **request_body,
                "responses": {
                    200: {
                        "content": {
                            "application/json": {
                                "schema": cls._response.model_json_schema(),
                                "examples": {
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
                            }
                        },
                    },
                },
            },
        }
