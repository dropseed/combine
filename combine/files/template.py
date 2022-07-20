import jinja2
from ..jinja.references import get_references_in_path
from .ignored import IgnoredFile


class TemplateFile(IgnoredFile):
    def load(self, jinja_environment: jinja2.Environment) -> None:
        self.references = get_references_in_path(self.path, jinja_environment)

    def _render_to_output(
        self, output_path: str, jinja_environment: jinja2.Environment
    ) -> str:
        return ""
