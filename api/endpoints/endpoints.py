import inspect
import random
from functools import wraps
from time import time
from typing import Any, Callable, Self

import loguru
from flask import Blueprint
from flask import Response as FlaskResponse
from flask import make_response, request

from api.context import Context
from api.controllers.controller import Controller
from api.database.repository import DatabaseRepository
from api.docs.models import EndpointDict
from api.errors import APIError
from api.schemas import Response

controllers: dict[str, type[Controller]] = {}


class Color:
    WHITE = "\x1b[37;20m"
    GRAY = "\x1b[90;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    TEAL = "\x1b[36;20m"
    BLUE = "\x1b[34;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"


def colorize(text: Any, color: str) -> str:
    return color + str(text) + Color.RESET


def colorize_method(method: str) -> str:
    method_text = f"{method:<8}"
    match method:
        case "GET":
            return colorize(method_text, Color.BLUE)
        case "POST":
            return colorize(method_text, Color.GREEN)
        case "PUT":
            return colorize(method_text, Color.YELLOW)
        case "PATCH":
            return colorize(method_text, Color.TEAL)
        case "DELETE":
            return colorize(method_text, Color.RED)
    return colorize(method, Color.GRAY)


def colorize_code(status_code: int) -> str:
    if status_code >= 400 and status_code < 500:
        return colorize(status_code, Color.RED)
    if status_code >= 300:
        return colorize(status_code, Color.YELLOW)
    if status_code >= 200:
        return colorize(status_code, Color.GREEN)

    return colorize(status_code, Color.BOLD_RED)


def colorize_time(duration: float) -> str:
    duration_ms = duration * 1000
    duration_text = f"{duration_ms:.02f} ms"
    if duration_ms > 1000:
        return colorize(duration_text, Color.RED)
    if duration_ms > 200:
        return colorize(duration_text, Color.YELLOW)
    return colorize(duration_text, Color.GREEN)


class Endpoints:
    def __init__(self, name: str, prefix: str) -> None:
        self.blueprint = Blueprint(name, name, url_prefix=prefix)
        self.prefix = prefix

    def route(self, endpoint: str, func: Callable):
        method, path = endpoint.split(" ")
        self.blueprint.route(path, methods=[method.upper()])(func)

    @property
    def docs(self) -> list[EndpointDict]:
        return [controller.get_docs() for controller in controllers.values()]

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
                    DatabaseRepository(ctx) as r,
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
            logger.info(
                f"{colorize_method(request.method)} {request.path}"
                f" {colorize_code(code)}"
                f" ({colorize_time(time() - start)})"
            )
            if isinstance(result, FlaskResponse):
                return result
            if isinstance(result, Response):
                return make_response(result.to_dict())
            return make_response(result)

        return wrapper
