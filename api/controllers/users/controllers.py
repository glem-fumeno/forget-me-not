from api.controllers.facade import Facade
from api.controllers.users.delete import UserDeleteController
from api.controllers.users.login import UserLoginController
from api.controllers.users.read import UserReadController
from api.controllers.users.read_me import UserReadMeController
from api.controllers.users.register import UserRegisterController
from api.controllers.users.search import UserSearchController
from api.controllers.users.set_user_cart import CartSetUserCartController
from api.controllers.users.update import UserUpdateController


class UserControllers(Facade):
    register = UserRegisterController.run
    read = UserReadController.run
    read_me = UserReadMeController.run
    update = UserUpdateController.run
    delete = UserDeleteController.run
    login = UserLoginController.run
    search = UserSearchController.run
    set_user_cart = CartSetUserCartController.run
