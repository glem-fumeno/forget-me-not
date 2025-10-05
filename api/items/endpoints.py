from fastapi import APIRouter

from api.repository import Repository


class ItemEndpoints:
    def __init__(self, repository: Repository) -> None:
        router = APIRouter(prefix="/items")
        items = repository.items
        self.router = router

        router.post("")(items.create)
        router.get("")(items.search)
        router.get("/{item_id}")(items.read)
        router.put("/{item_id}")(items.update)
        router.delete("/{item_id}")(items.delete)
