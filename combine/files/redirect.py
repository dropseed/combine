import os

from .html import HTMLFile
from .utils import create_parent_directory


class RedirectFile(HTMLFile):
    def get_render_variables(self):
        variables = super().get_render_variables()
        variables["redirect_url"] = open(self.path, "r").read().strip()
        return variables

    def get_template_path(self):
        return "redirect.template.html"
