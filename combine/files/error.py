import os
import traceback

from .html import HTMLFile
from .utils import create_parent_directory


class ErrorFile(HTMLFile):
    def __init__(self, *args, **kwargs):
        self.error = kwargs.pop("error")
        super().__init__(*args, **kwargs)

    def _render_to_output(self, output_path, jinja_environment):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        template = jinja_environment.get_template("error.template.html")

        with open(target_path, "w+") as f:
            if hasattr(self.error, "source"):
                context_lines = "\n".join(
                    self.error.source.splitlines()[
                        max(self.error.lineno - 3, 0) : self.error.lineno + 3
                    ]
                )
            else:
                context_lines = ""

            f.write(
                template.render(
                    error=self.error,
                    relative_path=self.content_relative_path,
                    context_lines=context_lines,
                    excinfo=traceback.format_exc(),
                )
            )

        return target_path
