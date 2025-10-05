import os

from api.core.call import Call


class FileDeleteCall(Call):
    def run(self, file_id: int):
        cursor = self.cursor.execute(self.query, (file_id,))
        (url,) = cursor.fetchone()
        os.remove(
            f"{self.config['FILE_DIRECTORY']}{file_id}.{url.split('.')[-1]}"
        )

    @property
    def query(self) -> str:
        return """
            DELETE FROM files_ WHERE file_id_ = ? RETURNING url_
        """
