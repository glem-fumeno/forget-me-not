from api.controllers.repository import Controller
from api.errors import LoggedOut


class CartController(Controller):

    def validate_access(self):
        issuer = self.repository.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut
        self.issuer = issuer
