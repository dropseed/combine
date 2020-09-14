import os
import traceback

from .html import HTMLFile
from .utils import create_parent_directory


class ErrorFile(HTMLFile):
    def __init__(self, *args, **kwargs):
        self.error = kwargs.pop("error")
        super().__init__(*args, **kwargs)

    def render_to_output(self, output_path, *args, **kwargs):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        template = kwargs["jinja_environment"].get_template("error.template.html")

        with open(target_path, "w+") as f:
            context_lines = "\n".join(
                self.error.source.splitlines()[
                    max(self.error.lineno - 3, 0) : self.error.lineno + 3
                ]
            )
            f.write(
                template.render(
                    error=self.error,
                    relative_path=self.content_relative_path,
                    context_lines=context_lines,
                    excinfo=traceback.format_exc(),
                )
            )
