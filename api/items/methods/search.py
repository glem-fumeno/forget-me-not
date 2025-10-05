from api.core.method import Method
from api.items.models import ItemResponse


class ItemSearchMethod(Method):
    async def run(self) -> list[ItemResponse]:
        results = self.agent.items.select_many()
        return [
            ItemResponse(
                item_id=result.item_id, name=result.name, icon=result.icon
            )
            for result in results.values()
        ]
