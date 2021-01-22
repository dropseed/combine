from ..jinja.references import get_references_in_path
from .ignored import IgnoredFile


class TemplateFile(IgnoredFile):
    def _render_to_output(self, output_path, jinja_environment):
        self.references = get_references_in_path(self.path, jinja_environment)
