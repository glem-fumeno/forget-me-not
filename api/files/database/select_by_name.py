from api.core.call import Call
from api.files.models import FileModel


class FileSelectByNameCall(Call):
    def run(self, name: str) -> FileModel | None:
        cursor = self.cursor.execute(self.query, (name,))
        result = cursor.fetchone()
        if result is None:
            return
        (file_id, url) = result
        return FileModel(file_id, name, url)

    @property
    def query(self) -> str:
        return """
            SELECT file_id_, url_ FROM files_ WHERE name_ = ?
        """
