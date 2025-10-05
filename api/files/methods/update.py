from fastapi import HTTPException

from api.core.method import Method
from api.files.models import FileModel, FileRequest, FileResponse


class FileUpdateMethod(Method):
    async def run(self, file_id: int, request: FileRequest) -> FileResponse:
        file = self.agent.files.select(file_id)
        if file is None:
            raise HTTPException(404, "File not found")
        duplicate = self.agent.files.select_by_name(request.name)
        if duplicate is not None and duplicate.file_id != file_id:
            raise HTTPException(409, "File already exists")
        model = FileModel(file_id, request.name, "")
        self.agent.files.update(model)
        result = self.agent.files.select(file_id)
        assert result is not None
        return FileResponse(result.file_id, result.name, result.url)
