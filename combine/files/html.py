import os

from ..jinja.references import get_references_in_path
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

    def render_to_output(self, output_path, *args, **kwargs):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        template = kwargs["jinja_environment"].get_template(self.content_relative_path)

        with open(target_path, "w+") as f:
            f.write(template.render(url=self._get_url()))

        self.references = get_references_in_path(self.path, kwargs["jinja_environment"])

    #     self.load_references(jinja_env=kwargs["jinja_environment"])

    # def load_references(self, jinja_env):
    #     with open(self.path, "r") as f:
    #         ast = jinja_env.parse(f.read())
    #         self.references = list(meta.find_referenced_templates(ast))

    def _get_url(self):
        url = "/" + self.output_relative_path
        if url.endswith("/index.html"):
            url = url[:-10]
        return url
