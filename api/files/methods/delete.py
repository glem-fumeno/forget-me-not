from fastapi import HTTPException

from api.core.method import Method
from api.files.models import FileResponse


class FileDeleteMethod(Method):
    async def run(self, file_id: int) -> FileResponse:
        result = self.agent.files.select(file_id)
        if result is None:
            raise HTTPException(404, "File not found")
        self.agent.files.delete(file_id)
        return FileResponse(
            file_id=result.file_id, name=result.name, url=result.url
        )
