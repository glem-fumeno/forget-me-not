from typing import Literal

from api.schemas import Model

RoleLiteral = Literal["new", "user", "admin"]


class UserModel(Model):
    user_id: int
    cart_id: int | None
    username: str
    email: str
    password: str
    role: RoleLiteral

    @property
    def parameters(self) -> tuple[str, str, str, str]:
        return (self.username, self.email, self.password, self.role)
