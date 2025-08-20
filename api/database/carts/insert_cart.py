from api.database.operation import DatabaseOperation
from api.models.carts.models import CartModel


class CartInsertCartOperation(DatabaseOperation):
    def run(self, model: CartModel):
        result = self.cursor.execute(self.query, model.parameters)
        assert result.lastrowid is not None, "could not insert cart"
        model.cart_id = result.lastrowid

    @property
    def query(self) -> str:
        return """
            INSERT INTO carts_ (name_, icon_)
            VALUES (?, ?)
        """
