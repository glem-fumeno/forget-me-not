import faker

from api.models.carts.requests import CartCreateRequest
from api.models.items.requests import ItemCreateRequest
from api.models.recipes.requests import RecipeCreateRequest
from api.models.users.requests import UserLoginRequest


class Faker:
    def __init__(self) -> None:
        self.faker = faker.Faker()

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
