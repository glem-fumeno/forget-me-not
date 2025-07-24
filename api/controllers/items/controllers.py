
from api.controllers.facade import Facade
from api.controllers.items.create import ItemCreateController
from api.controllers.items.delete import ItemDeleteController
from api.controllers.items.read import ItemReadController
from api.controllers.items.search import ItemSearchController
from api.controllers.items.update import ItemUpdateController


class ItemControllers(Facade):
    create = ItemCreateController.run
    read = ItemReadController.run
    update = ItemUpdateController.run
    delete = ItemDeleteController.run
    search = ItemSearchController.run
