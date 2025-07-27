from api.schemas import Model


class CartModel(Model):
    cart_id: int
    name: str
    icon: str

    @property
    def parameters(self) -> tuple[str, str]:
        return (self.name, self.icon)


class CartItemModel(Model):
    item_id: int
    origin: str | None

    @property
    def parameters(self) -> tuple[int, str | None]:
        return (self.item_id, self.origin)
