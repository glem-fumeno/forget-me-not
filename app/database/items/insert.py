from app.database.query import Query
from app.schemas.items.models import ItemModel


class ItemInsertQuery(Query):
    async def run(self, model: ItemModel) -> int:
        result = await self.fetchval(
            model.name, model.icon, model.created_at, model.updated_at
        )
        assert result is not None
        return result

    @property
    def query(self) -> str:
        return """
            INSERT INTO fmn_item_ (name_, icon_, created_at_, updated_at_)
            VALUES (?, ?, ?, ?)
            RETURNING item_id_
        """
