import faker

from api.models.carts.models import CartModel
from api.models.carts.requests import CartCreateRequest
from api.models.items.models import ItemModel
from api.models.items.requests import ItemCreateRequest
from api.models.recipes.models import RecipeModel
from api.models.recipes.requests import RecipeCreateRequest
from api.models.users.models import UserModel
from api.models.users.requests import UserLoginRequest
from api.security import get_hash


class Faker:
    def __init__(self) -> None:
        self.faker = faker.Faker()

    @property
    def cart_model(self):
        return CartModel(cart_id=-1, name=self.noun, icon=self.icon)

    @property
    def recipe_model(self):
        return RecipeModel(recipe_id=-1, name=self.noun, icon=self.icon)

    @property
    def item_model(self):
        return ItemModel(item_id=-1, name=self.noun, icon=self.icon)

    @property
    def user_model(self):
        return UserModel(
            user_id=-1,
            cart_id=None,
            username=self.username,
            email=self.email,
            password=get_hash(self.password),
            role="user",
        )

    @property
    def cart(self):
        return CartCreateRequest(name=self.noun, icon=self.icon)

    @property
    def recipe(self):
        return RecipeCreateRequest(name=self.noun, icon=self.icon)

    @property
    def item(self):
        return ItemCreateRequest(name=self.noun, icon=self.icon)

    @property
    def login(self):
        return UserLoginRequest(email=self.email, password=self.password)

    @property
    def noun(self):
        return self.faker.catch_phrase()

    @property
    def icon(self):
        return self.faker.image_url()

    @property
    def email(self):
        return self.faker.email()

    @property
    def username(self):
        return self.faker.user_name()

    @property
    def password(self):
        return self.faker.password()
