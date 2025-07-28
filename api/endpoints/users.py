from flask import make_response, request

from api.controllers.users.delete import UserDeleteController
from api.controllers.users.login import UserLoginController
from api.controllers.users.read import UserReadController
from api.controllers.users.read_me import UserReadMeController
from api.controllers.users.register import UserRegisterController
from api.controllers.users.search import UserSearchController
from api.controllers.users.set_user_cart import CartSetUserCartController
from api.controllers.users.update import UserUpdateController
from api.endpoints.endpoints import Endpoints
from api.models.users.requests import UserLoginRequest, UserUpdateRequest
from config import get_config

config = get_config()


class UserEndpoints(Endpoints):
    def __init__(self) -> None:
        super().__init__("users", "/users")
        self.route("post /login", self.login)
        self.route("post /register", self.register)
        self.route("get /search", self.search)
        self.route("get /me", self.read_me)
        self.route("get /<user_id>", self.read)
        self.route("patch /<user_id>", self.update)
        self.route("delete /<user_id>", self.delete)
        self.route("put /cart/<cart_id>", self.put_cart)

    @Endpoints.handler
    def register(self, controller: UserRegisterController):
        response_ = controller.run(UserLoginRequest.from_flask(request))
        response = make_response(response_.to_dict())
        response.set_cookie(
            key="token",
            value=response_.token,
            domain=config.FRONTEND_URL.removeprefix("https://"),
        )
        return response

    @Endpoints.handler
    def login(self, controller: UserLoginController):
        response_ = controller.run(UserLoginRequest.from_flask(request))
        response = make_response(response_.to_dict())
        response.set_cookie(
            key="token",
            value=response_.token,
            domain=config.FRONTEND_URL.removeprefix("https://"),
        )
        return response

    @Endpoints.handler
    def search(self, controller: UserSearchController):
        return controller.run()

    @Endpoints.handler
    def read(self, controller: UserReadController, user_id: int):
        return controller.run(user_id)

    @Endpoints.handler
    def read_me(self, controller: UserReadMeController):
        return controller.run()

    @Endpoints.handler
    def update(self, controller: UserUpdateController, user_id: int):
        return controller.run(user_id, UserUpdateRequest.from_flask(request))

    @Endpoints.handler
    def put_cart(self, controller: CartSetUserCartController, cart_id: int):
        return controller.run(cart_id)

    @Endpoints.handler
    def delete(self, controller: UserDeleteController, user_id: int):
        return controller.run(user_id)


endpoints = UserEndpoints()
