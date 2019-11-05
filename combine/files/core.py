import os
from shutil import copyfile

import babel

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

        self.locale = self.get_locale()

    def get_path_for_output(self):
        return self.content_relative_path

    def get_locale(self):
        head, tail = os.path.split(self.content_relative_path)
        while head or tail:
            try:
                # return the first directory with a valid locale for the name
                return babel.Locale.parse(tail)
            except (babel.UnknownLocaleError, ValueError):
                pass

            head, tail = os.path.split(head)

        return None

    def render_to_output(self, output_path, combine):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        if os.path.exists(target_path):
            os.remove(target_path)

        copyfile(self.path, target_path)
