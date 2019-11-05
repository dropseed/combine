import os

from .core import File
from .utils import create_parent_directory


class HTMLFile(File):
    def get_path_for_output(self):
        if self.name_without_extension.endswith(".keep"):
            # remove .keep.html from the end and replace with .html
            return super().get_path_for_output()[:-10] + ".html"

        if self.name_without_extension == "index":
            return super().get_path_for_output()

        return os.path.join(*self.root_parts, "index.html")

    def get_render_variables(self):
        return {"url": self._get_url(), "locale": self.locale}

    def get_template_path(self):
        return self.content_relative_path

    def render_to_output(self, output_path, combine):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        template_path = self.get_template_path()
        template = combine.jinja_environment.get_template(template_path)

        if self.locale:
            combine.install_translations(self.locale)

        variables = self.get_render_variables()

        with open(target_path, "w+") as f:
            f.write(template.render(**variables))

    def _get_url(self):
        url = "/" + self.output_relative_path
        if url.endswith("/index.html"):
            url = url[:-10]
        return url
