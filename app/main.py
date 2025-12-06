from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from app.schemas.payload import BasicResponse
from app.api.lifespan import lifespan
from app.api.middleware import acquire, catch_errors, log
from app.endpoints import router
from app.logger import init_logger

init_logger()

_openapi = FastAPI.openapi


def openapi(self: FastAPI):
    _openapi(self)
    assert self.openapi_schema is not None

    for _, method_item in self.openapi_schema["paths"].items():
        for _, param in method_item.items():
            if "422" in param["responses"]:
                del param["responses"]["422"]

    return self.openapi_schema


FastAPI.openapi = openapi

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "syntaxHighlight": {"theme": "nord"},
        "tryItOutEnabled": True,
        "requestSnippetsEnabled": True,
        "requestSnippets": {
            "generators": {
                "curl_bash": {"title": "", "syntax": "bash"},
            },
            "defaultExpanded": False,
            "languages": ["curl_bash"],
        },
    },
)

app.middleware("http")(log)
app.middleware("http")(acquire)
app.middleware("http")(catch_errors)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    _, exc: RequestValidationError
) -> JSONResponse:
    errors = []
    for err in exc.errors():
        errors.append(
            {"location": ".".join(err["loc"][1:]), "detail": err["msg"]}
        )
    return JSONResponse(status_code=422, content=errors)


@app.get("/", include_in_schema=False)
async def get_root():
    return RedirectResponse("/docs")


@app.get("/echo")
async def echo(message: str) -> BasicResponse:
    return BasicResponse(message=message)


app.include_router(router.items)
