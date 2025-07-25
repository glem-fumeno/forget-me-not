from api.controllers.controller import Controller
from api.errors import Inaccessible, LoggedOut


class ItemController(Controller):

    def validate_access(self, admin: bool = True):
        issuer = self.repository.users.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut
        if admin and issuer.role != "admin":
            raise Inaccessible
