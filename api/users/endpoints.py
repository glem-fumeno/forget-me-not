import uuid

from flask import Blueprint, Response, make_response, request

from api.schemas import Error
from api.users.schemas.errors import InvalidCredentialsError, UserExistsError
from api.users.schemas.models import UserModel
from api.users.schemas.requests import UserLoginRequest
from api.users.schemas.responses import UserResponse

users = Blueprint("users", "users", url_prefix="/users")

max_user_id: int = 0
user_map: dict[int, UserModel] = {}
email_map: dict[str, int] = {}
user_login_map: dict[str, int] = {}


def insert_user(user: UserModel):
    global max_user_id
    max_user_id += 1
    user_map[max_user_id] = user
    email_map[user.email] = max_user_id
    user.user_id = max_user_id


def insert_session(user_id: int):
    session_uuid = uuid.uuid4().hex
    user_login_map[session_uuid] = user_id
    return session_uuid


def response_from_error(error: type[Error]) -> Response:
    return make_response({"error": error.MESSAGE}, error.CODE)


@users.post("/register")
def register():
    request_ = UserLoginRequest.from_flask(request)
    model_ = UserModel(0, request_.email, request_.email, request_.password)
    if request_.email in email_map:
        return response_from_error(UserExistsError)
    insert_user(model_)
    session_uuid = insert_session(model_.user_id)
    response_ = UserResponse(
        model_.user_id, model_.username, model_.email
    ).to_dict()
    response = make_response(response_)
    response.set_cookie(key="token", value=session_uuid)
    return response


@users.post("/login")
def login():
    request_ = UserLoginRequest.from_flask(request)
    user_id = email_map.get(request_.email)
    if user_id is None:
        return response_from_error(InvalidCredentialsError)
    model_ = user_map[user_id]
    if model_.password != request_.password:
        return response_from_error(InvalidCredentialsError)
    session_uuid = insert_session(user_id)
    response_ = UserResponse(user_id, model_.username, model_.email).to_dict()
    response = make_response(response_)
    response.set_cookie(key="token", value=session_uuid)
    return response
