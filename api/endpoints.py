import inspect
import random
from functools import wraps
from typing import Callable

from flask import Blueprint
from flask import Response as FlaskResponse
from flask import make_response, request

from api.context import Context
from api.controller import Controller
from api.database.repository import DatabaseRepository
from api.docs.models import EndpointDict
from api.errors import APIError
from api.schemas import Response


class Endpoints:
    def __init__(
        self, name: str, prefix: str, repository: DatabaseRepository
    ) -> None:
        self.repository = repository
        self.blueprint = Blueprint(name, name, url_prefix=prefix)
        self.prefix = prefix
        self.controllers: dict[str, type[Controller]] = {}

    def route(self, endpoint: str, func: Callable):
        method, path = endpoint.split(" ")
        self.blueprint.route(path, methods=[method.upper()])(func)

    @property
    def docs(self) -> list[EndpointDict]:
        return [
            controller.get_docs() for controller in self.controllers.values()
        ]

    @staticmethod
    def handler(func: Callable):
        signature = inspect.signature(func)
        expected_types = {
            key: parameter.annotation
            for key, parameter in signature.parameters.items()
        }
        if "controller" not in expected_types:
            raise KeyError("Controller not found")
        controller = expected_types["controller"]
        if not issubclass(controller, Controller):
            raise TypeError("Controller is not a subclass of Controller")

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self.repository as r:
                ctx = Context()
                ctx = ctx.add("hash", f"{random.getrandbits(32):08x}")
                if "token" in request.cookies:
                    ctx = ctx.add("token", request.cookies["token"])
                kwargs = {
                    k: expected_types[k](v) if k in expected_types else v
                    for k, v in kwargs.items()
                }
                try:
                    result = func(self, controller(ctx, r), *args, **kwargs)
                except APIError as error:
                    return make_response({"error": error.MESSAGE}, error.CODE)
            if isinstance(result, FlaskResponse):
                return result
            if isinstance(result, Response):
                return make_response(result.to_dict())
            return make_response(result)

        return wrapper
