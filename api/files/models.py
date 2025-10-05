from dataclasses import dataclass


@dataclass
class FileModel:
    file_id: int
    name: str
    url: str


@dataclass
class FileRequest:
    name: str


@dataclass
class FileResponse:
    file_id: int
    name: str
    url: str
