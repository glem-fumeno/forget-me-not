from flask import Blueprint, send_file

from api.users.docs import endpoints

docs = Blueprint("docs", "docs", url_prefix="/docs")


@docs.route("/openapi.json")
def openapi():
    response = {
        "openapi": "3.1.0",
        "info": {"title": "Sample API"},
        "paths": {},
    }
    for endpoint_info in endpoints:
        method, endpoint = endpoint_info["endpoint"].split(" ")
        _, tag, _ = endpoint.split("/", 3)

        if endpoint not in response["paths"]:
            response["paths"][endpoint] = {}

        if method not in response["paths"][endpoint]:
            response["paths"][endpoint][method] = {}
        parameters = []
        if "path" in endpoint_info:
            parameters += [
                {"in": "path", "name": key, "schema": {"type": value}}
                for key, value in endpoint_info["path"].items()
            ]
        if "query" in endpoint_info:
            parameters += [
                {"in": "query", "name": key, "schema": {"type": value}}
                for key, value in endpoint_info["query"].items()
            ]
        responses = {
            "200": {"value": endpoint_info["responses"].get_example()}
        }
        for e in endpoint_info["errors"]:
            responses[f"{e.CODE} {e.__name__}"] = {
                "value": {"error": e.MESSAGE}
            }

        response["paths"][endpoint][method] = {
            "tags": [tag],
            "parameters": parameters,
            "requestBody": (
                {
                    "content": {
                        "application/json": {
                            "examples": {
                                k: {"value": v}
                                for k, v in endpoint_info["body"]
                                .get_examples()
                                .items()
                            }
                        }
                    }
                }
                if "body" in endpoint_info
                else None
            ),
            "responses": {
                "200": {
                    "content": {"application/json": {"examples": responses}}
                }
            },
        }
    return response


@docs.get("/")
def swagger():
    return send_file("api/docs/static/swagger.html")


@docs.get("/swagger.js")
def swagger_js():
    return send_file("api/docs/static/swagger.js")


@docs.get("/style.css")
def swagger_css():
    return send_file("api/docs/static/swagger.css")


@docs.get("/tags.js")
def swagger_tags():
    return send_file("api/docs/static/tags.js")
