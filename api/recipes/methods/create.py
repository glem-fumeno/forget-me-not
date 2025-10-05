from fastapi import HTTPException

from api.core.method import Method
from api.recipes.models import RecipeModel, RecipeRequest, RecipeResponse


class RecipeCreateMethod(Method):
    async def run(self, request: RecipeRequest) -> RecipeResponse:
        model = RecipeModel(recipe_id=-1, name=request.name, icon=request.icon)
        duplicate = self.agent.recipes.select_by_name(request.name)
        if duplicate is not None:
            raise HTTPException(409, "Recipe already exists")
        self.agent.recipes.insert(model)
        result = self.agent.recipes.select(model.recipe_id)
        assert result is not None, "could not insert recipe"
        return RecipeResponse(
            recipe_id=result.recipe_id,
            name=result.name,
            icon=result.icon,
            items=[],
        )
