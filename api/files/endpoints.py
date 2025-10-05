from fastapi import APIRouter

from api.repository import Repository


class FileEndpoints:
    def __init__(self, repository: Repository) -> None:
        router = APIRouter(prefix="/files")
        files = repository.files
        self.router = router

        router.post("")(files.create)
        router.get("")(files.search)
        router.put("/{file_id}")(files.update)
        router.delete("/{file_id}")(files.delete)
