from fastapi import FastAPI

from api.agent import Agent
from api.cart.endpoints import CartEndpoints
from api.files.endpoints import FileEndpoints
from api.items.endpoints import ItemEndpoints
from api.recipes.endpoints import RecipeEndpoints
from api.repository import Repository

app = FastAPI()
agent = Agent()
repository = Repository(agent)

app.include_router(ItemEndpoints(repository).router)
app.include_router(RecipeEndpoints(repository).router)
app.include_router(CartEndpoints(repository).router)
app.include_router(FileEndpoints(repository).router)
