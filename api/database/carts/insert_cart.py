from api.models.carts.models import CartModel
from api.database.operation import DatabaseOperation


class CartInsertCartOperation(DatabaseOperation):
    def run(self, user_id: int, model: CartModel):
        result = self.cursor.execute(self.query, model.parameters)
        assert result.lastrowid is not None, "could not insert cart"
        model.cart_id = result.lastrowid
        self.cursor.execute(self.user_query, (model.cart_id, user_id))

    @property
    def query(self) -> str:
        return """
            INSERT INTO carts_ (name_, icon_)
            VALUES (?, ?)
        """

    @property
    def user_query(self) -> str:
        return """
            INSERT INTO carts_users_ (cart_id_, user_id_)
            VALUES (?, ?)
        """
