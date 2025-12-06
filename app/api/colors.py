from http import HTTPStatus
from typing import Any, Literal

Color = Literal[
    "white",
    "gray",
    "green",
    "yellow",
    "teal",
    "purple",
    "blue",
    "red",
    "bold_red",
    "reset",
]
colors: dict[Color, str] = {
    "white": "\x1b[37;20m",
    "gray": "\x1b[90;20m",
    "green": "\x1b[32;20m",
    "yellow": "\x1b[33;20m",
    "teal": "\x1b[36;20m",
    "purple": "\x1b[35;20m",
    "blue": "\x1b[34;20m",
    "red": "\x1b[31;20m",
    "bold_red": "\x1b[31;1m",
    "reset": "\x1b[0m",
}

methods: dict[str, Color] = {
    "GET": "blue",
    "POST": "green",
    "PUT": "yellow",
    "PATCH": "teal",
    "DELETE": "red",
}

codes: dict[int, Color] = {
    200: "green",
    300: "yellow",
    400: "red",
    500: "bold_red",
}
times: dict[int, Color] = {
    0: "green",
    100: "yellow",
    200: "red",
}


def colorize(text: Any, color: Color) -> str:
    return colors[color] + str(text) + colors["reset"]


def colorize_method(method: str) -> str:
    return colorize(f"{method:<8}", methods.get(method, "gray"))


def colorize_code(code: int) -> str:
    return colorize(
        f"{code} {HTTPStatus(code).phrase}",
        codes.get(code - code % 100, "bold_red"),
    )


def colorize_time(t: float) -> str:
    t *= 1000
    return colorize(f"{t:6.2f} ms ", times.get(int(t - t % 100), "red"))
