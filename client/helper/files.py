from os import makedirs
from os.path import dirname, exists


def content(file_path: str, not_exist=None) -> str:
    if not exists(file_path):
        if not_exist is None:
            raise FileNotFoundError("File not found")
        return not_exist
    with open(file_path, "r") as file:
        return file.read()


def write(file_path: str, content_: str):
    if dirname(file_path):
        makedirs(dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content_)
