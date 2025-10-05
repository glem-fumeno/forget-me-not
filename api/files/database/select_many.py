from api.core.call import Call
from api.files.models import FileModel


class FileSelectManyCall(Call):
    def run(self) -> dict[int, FileModel]:
        cursor = self.cursor.execute(self.query)
        results = cursor.fetchall()
        return {
            file_id: FileModel(file_id, name, url)
            for (file_id, name, url) in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT file_id_, name_, url_ FROM files_
        """
