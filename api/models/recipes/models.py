from api.schemas import Model


class RecipeModel(Model):
    recipe_id: int
    name: str
    icon: str

    @property
    def parameters(self) -> tuple[str, str]:
        return (self.name, self.icon)


class RecipeUserModel(Model):
    recipe_id: int
    user_id: int

    @property
    def parameters(self) -> tuple[int, int]:
        return (self.recipe_id, self.user_id)
