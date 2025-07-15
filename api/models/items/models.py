from api.schemas import Model


class ItemModel(Model):
    item_id: int
    name: str
    icon: str

    @property
    def parameters(self) -> tuple[str, str]:
        return (self.name, self.icon)


class ItemUserModel(Model):
    item_id: int
    user_id: int

    @property
    def parameters(self) -> tuple[int, int]:
        return (self.item_id, self.user_id)
