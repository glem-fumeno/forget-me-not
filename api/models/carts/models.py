from api.schemas import Model


class CartModel(Model):
    cart_id: int
    name: str
    icon: str

    @property
    def parameters(self) -> tuple[str, str]:
        return (self.name, self.icon)
