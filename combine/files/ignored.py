from .core import File
import jinja2


class IgnoredFile(File):
    def _get_output_relative_path(self) -> str:
        return ""

    def _render_to_output(
        self, output_path: str, jinja_environment: jinja2.Environment
    ) -> str:
        return ""
