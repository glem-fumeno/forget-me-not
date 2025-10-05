from fastapi import HTTPException, UploadFile

from api.core.method import Method
from api.files.models import FileModel, FileResponse


class FileCreateMethod(Method):
    async def run(self, file: UploadFile) -> FileResponse:
        if file.filename is None:
            raise HTTPException(422, "No filename")
        if "." not in file.filename:
            raise HTTPException(422, "No extension")
        *name, extension = file.filename.split(".")
        name = ".".join(name)
        model = FileModel(-1, name, "")
        duplicate = self.agent.files.select_by_name(name)
        if duplicate is not None:
            raise HTTPException(409, "File already exists")
        self.agent.files.insert(model, file.file, extension)
        result = self.agent.files.select(model.file_id)
        assert result is not None, "could not insert file"
        return FileResponse(result.file_id, result.name, result.url)
