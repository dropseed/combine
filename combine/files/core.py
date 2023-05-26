import os
from shutil import copyfile
from typing import List, TYPE_CHECKING

import jinja2
from ..checks.issues import Issues
from ..checks.file_size import FileSizeCheck
from .utils import create_parent_directory
from ..checks.base import Check

if TYPE_CHECKING:
    from combine.core import ContentDirectory


class File:
    def __init__(self, path: str, content_directory: "ContentDirectory") -> None:
        self.path = path
        self.references: List[str] = []
        self.content_directory = content_directory
        self.content_relative_path = os.path.relpath(
            self.path, self.content_directory.path
        )

        self.root, self.extension = os.path.splitext(self.content_relative_path)
        self.root_parts = os.path.split(self.root)
        self.name_without_extension = self.root_parts[-1]

        self.output_relative_path = self._get_output_relative_path()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.path}>"

    def _get_output_relative_path(self) -> str:
        return self.content_relative_path

    def load(self, jinja_environment: jinja2.Environment) -> None:
        """Load properties that can vary depending on content of the file"""
        self.references = []

    def render(self, output_path: str, jinja_environment: jinja2.Environment) -> None:
        self.output_path = self._render_to_output(output_path, jinja_environment)

    def _render_to_output(
        self, output_path: str, jinja_environment: jinja2.Environment
    ) -> str:
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        if os.path.exists(target_path):
            os.remove(target_path)

        copyfile(self.path, target_path)

        return target_path

    def check_output(self) -> Issues:
        issues = Issues()

        for check in self.get_checks():
            for issue in check.run():
                issues.append(issue)

        if issues:
            issues.print(f"Issues in {self.content_relative_path}")

        return issues

    def get_checks(self) -> List[Check]:
        if self.output_path:
            # Not all files have an output
            return [
                FileSizeCheck(path=self.output_path),
            ]

        return []
