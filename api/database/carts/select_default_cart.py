from api.database.operation import DatabaseOperation
from api.models.carts.models import CartModel


class CartSelectDefaultCartOperation(DatabaseOperation):
    def run(self) -> CartModel | None:
        result = self.cursor.execute(self.query)
        columns = result.fetchone()
        if columns is None:
            return
        return CartModel.from_db(result.description, columns)

    @property
    def query(self) -> str:
        return """
            SELECT cart_id_, name_, icon_
            FROM metadata_
            INNER JOIN carts_ USING (cart_id_)
            WHERE metadata_id_ = 0
        """
