from ..jinja.references import get_references_in_path
from .ignored import IgnoredFile


class TemplateFile(IgnoredFile):
    def render_to_output(self, *args, **kwargs):
        self.references = get_references_in_path(self.path, kwargs["jinja_environment"])
