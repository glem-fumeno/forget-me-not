from typing import BinaryIO

from api.core.call import Call
from api.files.models import FileModel


class FileInsertCall(Call):
    def run(self, model: FileModel, file: BinaryIO, extension: str):
        cursor = self.cursor.execute(self.query, (model.name,))
        (file_id,) = cursor.fetchone()
        model.file_id = file_id
        model.url = f"{self.config['FILE_URL']}{file_id}.{extension}"
        self.cursor.execute(self.url_query, (model.url, file_id))
        with open(
            f"{self.config['FILE_DIRECTORY']}{file_id}.{extension}", "wb"
        ) as f:
            f.write(file.read())

    @property
    def query(self) -> str:
        return """
            INSERT INTO files_ (name_) VALUES (?) RETURNING file_id_
        """

    @property
    def url_query(self) -> str:
        return """
            UPDATE files_ SET url_ = ? WHERE file_id_ = ?
        """
