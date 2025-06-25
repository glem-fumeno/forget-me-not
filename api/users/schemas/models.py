from typing import Literal

from api.schemas import Model

RoleLiteral = Literal["new", "user", "admin"]

class UserModel(Model):
    user_id: int
    username: str
    email: str
    password: str
    role: RoleLiteral

    @property
    def parameters(self) -> tuple[str, str, str, str]:
        return (self.username, self.email, self.password, self.role)


class UserSessionModel(Model):
    user_id: int
    token: str

    @property
    def parameters(self) -> tuple[int, str]:
        return (self.user_id, self.token)
