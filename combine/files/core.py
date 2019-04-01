import os
from shutil import copyfile

from .utils import create_parent_directory


class File:
    def __init__(self, path, content_directory):
        self.path = path
        self.content_directory = content_directory
        self.content_relative_path = os.path.relpath(
            self.path, self.content_directory.path
        )

        self.root, self.extension = os.path.splitext(self.content_relative_path)
        self.root_parts = os.path.split(self.root)
        self.name_without_extension = self.root_parts[-1]

        self.output_relative_path = self.get_path_for_output()

    def get_path_for_output(self):
        return self.content_relative_path

    def render_to_output(self, output_path, *args, **kwargs):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        if os.path.exists(target_path):
            os.remove(target_path)

        copyfile(self.path, target_path)
