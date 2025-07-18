from api.models.carts.models import CartUserModel
from api.database.operation import DatabaseOperation


class CartInsertCartUserOperation(DatabaseOperation):
    def run(self, model: CartUserModel):
        self.cursor.execute(self.query, model.parameters)

    @property
    def query(self) -> str:
        return """
            INSERT INTO carts_users_ (cart_id_, user_id_)
            VALUES (?, ?)
        """
