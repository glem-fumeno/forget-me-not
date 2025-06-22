from dataclasses import dataclass

from api.schemas import Model


@dataclass
class CartModel(Model):
    cart_id: int
    name: str
    icon: str

    @property
    def parameters(self) -> tuple[str, str]:
        return (self.name, self.icon)

@dataclass
class CartUserModel(Model):
    cart_id: int
    user_id: int

    @property
    def parameters(self) -> tuple[int, int]:
        return (self.cart_id, self.user_id)
