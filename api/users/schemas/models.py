from dataclasses import dataclass

from api.schemas import Model


@dataclass
class UserModel(Model):
    user_id: int
    username: str
    email: str
    password: str

    @property
    def parameters(self) -> tuple[str, str, str]:
        return (self.username, self.email, self.password)


@dataclass
class UserSessionModel(Model):
    user_id: int
    token: str

    @property
    def parameters(self) -> tuple[int, str]:
        return (self.user_id, self.token)
