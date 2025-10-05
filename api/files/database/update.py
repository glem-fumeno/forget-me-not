from api.core.call import Call
from api.files.models import FileModel


class FileUpdateCall(Call):
    def run(self, model: FileModel):
        self.cursor.execute(self.query, (model.name, model.file_id))

    @property
    def query(self) -> str:
        return """
            UPDATE files_
            SET name_ = ?
            WHERE file_id_ = ?
        """
