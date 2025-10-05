from api.core.call import Call
from api.files.models import FileModel


class FileSelectCall(Call):
    def run(self, file_id: int) -> FileModel | None:
        cursor = self.cursor.execute(self.query, (file_id,))
        result = cursor.fetchone()
        if result is None:
            return
        (name, url) = result
        return FileModel(file_id, name, url)

    @property
    def query(self) -> str:
        return """
            SELECT name_, url_ FROM files_ WHERE file_id_ = ?
        """
