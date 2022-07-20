import os
import traceback

import jinja2
from .html import HTMLFile
from .utils import create_parent_directory

from typing import Any


class ErrorFile(HTMLFile):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.error = kwargs.pop("error")
        super().__init__(*args, **kwargs)

    def _render_to_output(
        self, output_path: str, jinja_environment: jinja2.Environment
    ) -> str:
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
