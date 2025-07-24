from api.controllers.controller import Controller
from api.errors import LoggedOut


class RecipeController(Controller):

    def validate_access(self):
        issuer = self.repository.users.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut
        self.issuer = issuer
