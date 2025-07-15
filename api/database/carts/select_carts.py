from api.models.carts.models import CartModel
from api.database.operation import DatabaseOperation


class CartSelectCartsOperation(DatabaseOperation):
    def run(self, user_id: int) -> dict[int, CartModel]:
        result = self.cursor.execute(self.query, (user_id,))
        results = result.fetchall()
        return {
            columns[0]: CartModel.from_db(result.description, columns)
            for columns in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT cart_id_, name_, icon_
            FROM carts_
            INNER JOIN carts_users_ USING (cart_id_)
            WHERE user_id_ = ?
        """
