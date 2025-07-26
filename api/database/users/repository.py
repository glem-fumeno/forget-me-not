from api.database.facade import Facade
from api.database.users.delete_user import UserDeleteUserOperation
from api.database.users.insert_user import UserInsertUserOperation
from api.database.users.insert_user_session import (
    UserInsertUserSessionOperation,
)
from api.database.users.select_user import UserSelectUserOperation
from api.database.users.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.database.users.select_user_id_by_email import (
    UserSelectUserIdByEmailOperation,
)
from api.database.users.select_users import UserSelectUsersOperation
from api.database.users.update_user import UserUpdateUserOperation
from api.database.users.update_user_cart import CartUpdateUserCartOperation


class UserRepository(Facade):
    insert_user = UserInsertUserOperation.run
    insert_user_session = UserInsertUserSessionOperation.run
    select_user = UserSelectUserOperation.run
    select_users = UserSelectUsersOperation.run
    select_user_id_by_email = UserSelectUserIdByEmailOperation.run
    select_user_by_token = UserSelectUserByTokenOperation.run
    update_user = UserUpdateUserOperation.run
    delete_user = UserDeleteUserOperation.run
    update_user_cart = CartUpdateUserCartOperation.run
