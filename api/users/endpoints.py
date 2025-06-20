from flask import Blueprint, Response, make_response, request

from api.schemas import APIError
from api.users.controllers.login import UserLoginController
from api.users.controllers.register import UserRegisterController
from api.users.database.core import UserDatabaseRepository
from api.users.schemas.requests import UserLoginRequest

users = Blueprint("users", "users", url_prefix="/users")


def response_from_error(error: APIError) -> Response:
    return make_response({"error": error.MESSAGE}, error.CODE)


@users.post("/register")
def register():
    try:
        with UserDatabaseRepository() as repository:
            controller = UserRegisterController(repository)
            response_ = controller.run(UserLoginRequest.from_flask(request))
    except APIError as e:
        return response_from_error(e)
    response = make_response(response_.to_dict())
    response.set_cookie(key="token", value=response_.token)
    return response


@users.post("/login")
def login():
    try:
        with UserDatabaseRepository() as repository:
            controller = UserLoginController(repository)
            response_ = controller.run(UserLoginRequest.from_flask(request))
    except APIError as e:
        return response_from_error(e)
    response = make_response(response_.to_dict())
    response.set_cookie(key="token", value=response_.token)
    return response
