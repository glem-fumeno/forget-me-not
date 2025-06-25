from api.carts.schemas.models import CartModel
from api.database.operation import DatabaseOperation


class CartUpdateCartOperation(DatabaseOperation):
    def run(self, model: CartModel):
        self.cursor.execute(self.query, (*model.parameters, model.cart_id))

    @property
    def query(self) -> str:
        return """
            UPDATE carts_
            SET
                name_ = ?,
                icon_ = ?
            WHERE
                cart_id_ = ?
        """
