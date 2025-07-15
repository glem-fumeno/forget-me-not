import inspect
import random
from functools import wraps
from time import time
from typing import Callable, Self

import loguru
from flask import Blueprint
from flask import Response as FlaskResponse
from flask import make_response, request

from api.context import Context
from api.controllers.repository import Controller
from api.database.repository import DatabaseRepository
from api.docs.models import EndpointDict
from api.errors import APIError
from api.schemas import Response

controllers: dict[str, type[Controller]] = {}

class Endpoints:
    def __init__(
        self, name: str, prefix: str, repository: type[DatabaseRepository]
    ) -> None:
        self.Repository = repository
        self.blueprint = Blueprint(name, name, url_prefix=prefix)
        self.prefix = prefix

    def route(self, endpoint: str, func: Callable):
        method, path = endpoint.split(" ")
        self.blueprint.route(path, methods=[method.upper()])(func)

    @property
    def docs(self) -> list[EndpointDict]:
        return [
            controller.get_docs() for controller in controllers.values()
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
        controllers[controller.__name__] = controller

        @wraps(func)
        def wrapper(self: Self, *args, **kwargs):
            ctx = Context()
            ctx = ctx.add("hash", f"{random.getrandbits(32):08x}")
            if "token" in request.cookies:
                ctx = ctx.add("token", request.cookies["token"])
            logger = loguru.logger.bind(hash=ctx.get("hash", "00000000"))
            start = time()
            kwargs = {
                k: expected_types[k](v) if k in expected_types else v
                for k, v in kwargs.items()
            }
            try:
                with (
                    self.Repository(ctx) as r,
                    logger.catch(exclude=APIError, reraise=True),
                ):
                    result = func(self, controller(ctx, r), *args, **kwargs)
                    code = 200
            except APIError as error:
                logger.debug(error.MESSAGE)
                result = make_response({"error": error.MESSAGE}, error.CODE)
                code = error.CODE
            except Exception:
                result = make_response({"error": "internal server error"}, 500)
                code = 500
            logger.info(f"{code}: {(time() - start) * 1000:.2f}ms")
            if isinstance(result, FlaskResponse):
                return result
            if isinstance(result, Response):
                return make_response(result.to_dict())
            return make_response(result)

        return wrapper
