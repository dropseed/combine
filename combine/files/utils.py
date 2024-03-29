import os


def create_parent_directory(path: str) -> None:
    path_dir = os.path.dirname(path)
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
