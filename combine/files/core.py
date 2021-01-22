import os
from shutil import copyfile

from ..checks.issues import Issues
from ..checks.file_size import FileSizeCheck
from .utils import create_parent_directory


class File:
    def __init__(self, path, content_directory):
        self.path = path
        self.references = []
        self.content_directory = content_directory
        self.content_relative_path = os.path.relpath(
            self.path, self.content_directory.path
        )

        self.root, self.extension = os.path.splitext(self.content_relative_path)
        self.root_parts = os.path.split(self.root)
        self.name_without_extension = self.root_parts[-1]

        self.output_relative_path = self._get_output_relative_path()

    def _get_output_relative_path(self):
        return self.content_relative_path

    def render(self, output_path, jinja_environment):
        self.output_path = self._render_to_output(output_path, jinja_environment)

    def _render_to_output(self, output_path, jinja_environment):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        if os.path.exists(target_path):
            os.remove(target_path)

        copyfile(self.path, target_path)

        return target_path

    def check_output(self):
        issues = Issues()

        for check in self.get_checks():
            for issue in check.run():
                issues.append(issue)

        if issues:
            issues.print(f"Issues in {self.content_relative_path}")

        return issues

    def get_checks(self):
        if self.output_path:
            # Not all files have an output
            return [
                FileSizeCheck(path=self.output_path),
            ]

        return []
