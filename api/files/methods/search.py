from api.core.method import Method
from api.files.models import FileResponse


class FileSearchMethod(Method):
    async def run(self) -> list[FileResponse]:
        results = self.agent.files.select_many()
        return [
            FileResponse(result.file_id, result.name, result.url)
            for result in results.values()
        ]
