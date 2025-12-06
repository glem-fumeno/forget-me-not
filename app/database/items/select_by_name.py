from app.database.query import Query
from app.schemas.items.models import ItemModel


class ItemSelectByNameQuery(Query):
    async def run(self, name: str) -> ItemModel | None:
        result = await self.fetchrow(name)
        if result is None:
            return None
        return ItemModel(
            item_id=result["item_id_"],
            name=result["name_"],
            icon=result["icon_"],
            created_at=result["created_at_"],
            updated_at=result["updated_at_"],
        )

    @property
    def query(self) -> str:
        return """
             SELECT item_id_, name_, icon_, created_at_, updated_at_
             FROM fmn_item_
             WHERE name_ = $1
        """
