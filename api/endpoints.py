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
from api.schemas import Response
from api.errors import APIError


class Endpoints:
    def __init__(
        self, name: str, prefix: str, repository: DatabaseRepository
    ) -> None:
        self.repository = repository
        self.blueprint = Blueprint(name, name, url_prefix=prefix)
        self.prefix = prefix
        self.controllers: dict[str, type[Controller]] = {}

    def route(
        self, endpoint: str, func: Callable, controller: type[Controller]
    ):
        method, path = endpoint.split(" ")
        self.blueprint.route(path, methods=[method.upper()])(func)
        self.controllers[func.__name__] = controller

    @property
    def docs(self) -> list[EndpointDict]:
        return [
            controller.get_docs() for controller in self.controllers.values()
        ]

    @staticmethod
    def handler(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self.repository as r:
                ctx = Context()
                ctx = ctx.add("hash", f"{random.getrandbits(32):08x}")
                if "token" in request.cookies:
                    ctx = ctx.add("token", request.cookies["token"])
                c = self.controllers[func.__name__](ctx, r)
                try:
                    result = func(self, c, *args, **kwargs)
                except APIError as error:
                    return make_response({"error": error.MESSAGE}, error.CODE)
            if isinstance(result, FlaskResponse):
                return result
            if isinstance(result, Response):
                return make_response(result.to_dict())
            return make_response(result)

        return wrapper
