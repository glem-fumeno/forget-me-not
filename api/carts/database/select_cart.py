from api.carts.schemas.models import CartModel
from api.database.operation import DatabaseOperation


class CartSelectCartOperation(DatabaseOperation):
    def run(self, user_id: int, cart_id: int) -> CartModel | None:
        result = self.cursor.execute(self.query, (cart_id, user_id))
        columns = result.fetchone()
        if columns is None:
            return
        return CartModel.from_db(result.description, columns)

    @property
    def query(self) -> str:
        return """
            SELECT cart_id_, name_, icon_
            FROM carts_
            INNER JOIN carts_users_ USING (cart_id_)
            WHERE cart_id_ = ? AND user_id_ = ?
        """
