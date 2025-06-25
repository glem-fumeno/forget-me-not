from flask import make_response, request

from api.endpoints import Endpoints
from api.users.controllers.delete import UserDeleteController
from api.users.controllers.login import UserLoginController
from api.users.controllers.read import UserReadController
from api.users.controllers.register import UserRegisterController
from api.users.controllers.search import UserSearchController
from api.users.controllers.update import UserUpdateController
from api.users.database.core import UserDatabaseRepository
from api.users.schemas.requests import UserLoginRequest, UserUpdateRequest


class UserEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__("users", "/users", UserDatabaseRepository)
        self.route("post /login", self.login)
        self.route("post /register", self.register)
        self.route("get /search", self.search)
        self.route("get /<user_id>", self.read)
        self.route("patch /<user_id>", self.update)
        self.route("delete /<user_id>", self.delete)

    @Endpoints.handler
    def register(self, controller: UserRegisterController):
        response_ = controller.run(UserLoginRequest.from_flask(request))
        response = make_response(response_.to_dict())
        response.set_cookie(key="token", value=response_.token)
        return response

    @Endpoints.handler
    def login(self, controller: UserLoginController):
        response_ = controller.run(UserLoginRequest.from_flask(request))
        response = make_response(response_.to_dict())
        response.set_cookie(key="token", value=response_.token)
        return response

    @Endpoints.handler
    def search(self, controller: UserSearchController):
        return controller.run()

    @Endpoints.handler
    def read(self, controller: UserReadController, user_id: int):
        return controller.run(user_id)

    @Endpoints.handler
    def update(self, controller: UserUpdateController, user_id: int):
        return controller.run(user_id, UserUpdateRequest.from_flask(request))

    @Endpoints.handler
    def delete(self, controller: UserDeleteController, user_id: int):
        return controller.run(user_id)


endpoints = UserEndpoints()
