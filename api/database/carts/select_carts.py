from api.database.operation import DatabaseOperation
from api.models.carts.models import CartModel


class CartSelectCartsOperation(DatabaseOperation):
    def run(self) -> dict[int, CartModel]:
        result = self.cursor.execute(self.query)
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
        """
