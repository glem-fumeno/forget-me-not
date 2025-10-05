from api.core.method import Method
from api.recipes.models import RecipeResponse


class RecipeSearchMethod(Method):
    async def run(self) -> list[RecipeResponse]:
        results = self.agent.recipes.select_many()
        return [
            RecipeResponse(
                recipe_id=result.recipe_id,
                name=result.name,
                icon=result.icon,
                items=[],
            )
            for result in results.values()
        ]
